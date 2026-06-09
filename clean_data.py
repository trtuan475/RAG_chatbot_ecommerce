import os

DATA_DIR = './data'
styles_in = os.path.join(DATA_DIR, 'styles.csv')
styles_out = os.path.join(DATA_DIR, 'styles_clean.csv')
images_in = os.path.join(DATA_DIR, 'images.csv')
images_out = os.path.join(DATA_DIR, 'images_clean.csv')

def clean_styles():
    if not os.path.exists(styles_in):
        print("No file styles.csv")
        return
    
    print("Cleaning styles.csv")
    with open(styles_in, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    clean_lines = []
    # giữ nguyên dòng tiêu đề 
    header = "id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName\n"
    clean_lines.append(header)
    
    success_count = 0
    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith('PL'): # bỏ qua các dòng rác 
            continue
            
        parts = line.split(',')
        # 10 cột data
        if len(parts) >= 10:
            # 9 cột đầu tiên giữ nguyên cấu trúc
            base_data = parts[0:9]
            # toàn bộ phần text còn lại bị phân tách bởi dấu phẩy sẽ được gộp lại thành cột thứ 10
            display_name = ",".join(parts[9:]).replace('"', '') # xoá "" nếu có
            
            # tạo chuỗi dữ liệu mới
            clean_line = f'{",".join(base_data)},"{display_name}"\n'
            clean_lines.append(clean_line)
            success_count += 1
            
    with open(styles_out, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    print(f"Done styles.csv! Count: {success_count}")

def clean_images():
    if not os.path.exists(images_in):
        print("No file images.csv")
        return
        
    print("Cleaning images.csv...")
    with open(images_in, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    clean_lines = []
    header = "filename,link\n"
    clean_lines.append(header)
    
    success_count = 0
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 2:
            filename = parts[0].replace('"', '')
            link = ",".join(parts[1:]).replace('"', '')
            clean_lines.append(f'"{filename}","{link}"\n')
            success_count += 1
            
    with open(images_out, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    print(f"Done images.csv! Count: {success_count}")

clean_styles()
clean_images()
