#!/bin/bash

# Renk Kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Ansible Reporting Automation Başlatılıyor...${NC}"

# Python3 kurulu mu kontrol et
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[HATA] Python3 sistemde kurulu değil. Lütfen önce Python3 kurun.${NC}"
    exit 1
fi

VENV_DIR="venv"

# Virtual environment yoksa oluştur
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Python Sanal Ortamı (venv) oluşturuluyor...${NC}"
    python3 -m venv $VENV_DIR
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[HATA] venv oluşturulamadı. Sisteminizde 'python3-venv' paketinin kurulu olduğundan emin olun.${NC}"
        exit 1
    fi
fi

# venv'i aktifleştir
echo -e "${YELLOW}Sanal ortam aktifleştiriliyor...${NC}"
source $VENV_DIR/bin/activate

# Gerekli pip paketlerini yükle
echo -e "${YELLOW}Gerekli kütüphaneler (ansible, pandas, openpyxl) kontrol ediliyor ve kuruluyor... (Bu işlem birkaç saniye sürebilir)${NC}"
pip install --upgrade pip --quiet
pip install ansible pandas openpyxl --quiet

if [ $? -ne 0 ]; then
    echo -e "${RED}[HATA] Kütüphaneler kurulurken bir sorun oluştu. İnternet bağlantınızı kontrol edin.${NC}"
    deactivate
    exit 1
fi

# Ansible playbook'u çalıştır
echo -e "${GREEN}Tüm gereksinimler hazır. Raporlama başlatılıyor...${NC}"
echo -e "----------------------------------------------------"
ansible-playbook rapor.yml
echo -e "----------------------------------------------------"

# Çıkışta venv'i kapat
deactivate
echo -e "${GREEN}İşlem başarıyla tamamlandı!${NC}"
