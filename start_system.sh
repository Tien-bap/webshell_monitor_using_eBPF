#!/bin/bash

# ============================================
#   AUTO START SYSTEM SCRIPT
#   Flask WebServer + Reverse Proxy + Monitor
# ============================================

set -e  # Dừng nếu có lỗi

# --- Màu sắc terminal ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- Cấu hình đường dẫn ---
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSERVER_DIR="$BASE_DIR/webserver"
REVERSE_PROXY_DIR="$BASE_DIR/reverse_proxy"
PROJECT_DIR="$BASE_DIR/project"

log_info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_success() { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "\n${CYAN}========== $1 ==========${NC}"; }

# --- Biến lưu bước hiện tại ---
CURRENT_STEP="khởi động"

# --- Trap: bắt lỗi, in bước bị lỗi rồi dừng ---
trap 'echo -e "\n${RED}[LỖI]${NC} Script thất bại tại bước: ${YELLOW}${CURRENT_STEP}${NC}\n       Dừng lại. Kiểm tra thông báo lỗi phía trên." ' ERR

# ============================================
# BƯỚC 1: Kiểm tra thư mục tồn tại
# ============================================
CURRENT_STEP="Kiểm tra thư mục"
log_step "$CURRENT_STEP"

for dir in "$WEBSERVER_DIR" "$REVERSE_PROXY_DIR" "$PROJECT_DIR"; do
    if [ ! -d "$dir" ]; then
        log_error "Không tìm thấy thư mục: $dir"
        log_warn "Hãy chỉnh lại BASE_DIR hoặc chạy script từ thư mục gốc của project."
        exit 1
    fi
    log_success "Tìm thấy: $dir"
done

# ============================================
# BƯỚC 2: Build Docker image flask-webserver
# ============================================
CURRENT_STEP="Build Docker Image (flask-webserver)"
log_step "$CURRENT_STEP"

if [ ! -f "$WEBSERVER_DIR/Dockerfile" ]; then
    log_error "Không tìm thấy Dockerfile trong $WEBSERVER_DIR"
    exit 1
fi

cd "$WEBSERVER_DIR"
log_info "Đang build image flask-webserver..."
docker build -t flask-webserver .
log_success "Build flask-webserver thành công!"

# ============================================
# BƯỚC 3: Chạy Docker Compose (Reverse Proxy)
# ============================================
CURRENT_STEP="Khởi động Docker Compose (Reverse Proxy)"
log_step "$CURRENT_STEP"

if [ ! -f "$REVERSE_PROXY_DIR/docker-compose.yml" ] && [ ! -f "$REVERSE_PROXY_DIR/compose.yml" ]; then
    log_error "Không tìm thấy docker-compose.yml trong $REVERSE_PROXY_DIR"
    exit 1
fi

cd "$REVERSE_PROXY_DIR"
log_info "Dừng các container cũ (nếu có)..."
docker compose down 2>/dev/null || true

log_info "Khởi động docker compose..."
docker compose up -d
log_success "Docker Compose khởi động thành công!"

# ============================================
# BƯỚC 4: Kiểm tra Web Server
# ============================================
CURRENT_STEP="Kiểm tra Web Server (localhost:8080)"
log_step "$CURRENT_STEP"

log_info "Chờ web server sẵn sàng..."
MAX_RETRY=15
COUNT=0
until curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 | grep -qE "^(200|301|302|304)$"; do
    COUNT=$((COUNT + 1))
    if [ $COUNT -ge $MAX_RETRY ]; then
        log_warn "Web server chưa phản hồi sau ${MAX_RETRY} lần thử. Tiếp tục..."
        break
    fi
    echo -n "."
    sleep 2
done
echo ""
log_success "Web server đang chạy tại http://localhost:8080"

# ============================================
# BƯỚC 5: Chạy Hệ Thống Giám Sát (main.py)
# ============================================
CURRENT_STEP="Khởi động Hệ Thống Giám Sát (main.py)"
log_step "$CURRENT_STEP"

if [ ! -f "$PROJECT_DIR/main.py" ]; then
    log_error "Không tìm thấy main.py trong $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

if [ "$EUID" -ne 0 ]; then
    log_warn "Tự động dùng sudo cho main.py..."
    SUDO_CMD="sudo"
else
    SUDO_CMD=""
fi

log_info "Khởi động hệ thống giám sát (main.py)..."
log_info "Nhấn Ctrl+C để dừng."
echo ""
$SUDO_CMD python3 main.py

# ============================================
# KẾT THÚC
# ============================================
log_step "Hệ thống đã dừng"
log_info "Dọn dẹp: tắt Docker Compose..."
cd "$REVERSE_PROXY_DIR"
docker compose down
log_success "Hoàn tất. Tạm biệt!"