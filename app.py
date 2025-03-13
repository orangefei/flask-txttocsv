# app.py
from flask import Flask, request, jsonify, send_file, render_template
import os
import csv
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert_file():
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({"error": "没有提供文件"}), 400
    
    file = request.files['file']
    
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    # 获取分隔符
    delimiter = request.form.get('delimiter', ',')
    
    # 获取输出编码
    output_encoding = request.form.get('encoding', 'utf-8')
    if output_encoding not in ['utf-8', 'gbk']:
        output_encoding = 'utf-8'  # 默认为utf-8
    
    # 安全地保存文件
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # 创建输出文件名
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_{output_encoding}.csv"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    
    try:
        # 尝试检测输入文件编码
        input_encoding = detect_encoding(file_path)
        
        # 转换文件
        line_count = convert_txt_to_csv(file_path, output_path, delimiter, input_encoding, output_encoding)
        
        # 返回结果
        return jsonify({
            "success": True,
            "message": f"已成功转换 {line_count} 行数据（输出编码：{output_encoding}）",
            "filename": output_filename,
            "encoding": output_encoding
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # 清理上传的文件
        try:
            os.remove(file_path)
        except:
            pass

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "文件不存在"}), 404
    
    # 发送文件
    response = send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )
    
    # 设置响应头，关闭缓存
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

def detect_encoding(file_path):
    """
    尝试检测文件编码，如果无法确定则默认使用UTF-8
    """
    try:
        from chardet import detect
        with open(file_path, 'rb') as file:
            # 读取部分文件内容进行编码检测
            raw_data = file.read(min(1024 * 1024, os.path.getsize(file_path)))
            result = detect(raw_data)
            return result['encoding'] or 'utf-8'
    except ImportError:
        # 如果没有安装chardet库，则默认返回UTF-8
        return 'utf-8'
    except Exception:
        # 如果检测失败，也默认返回UTF-8
        return 'utf-8'

def convert_txt_to_csv(input_file, output_file, delimiter=',', input_encoding='utf-8', output_encoding='utf-8'):
    """
    将TXT文件转换为CSV文件
    
    参数:
    input_file (str): 输入TXT文件路径
    output_file (str): 输出CSV文件路径
    delimiter (str): 分隔符，默认为逗号
    input_encoding (str): 输入文件编码
    output_encoding (str): 输出文件编码
    
    返回:
    int: 处理的行数
    """
    # 读取TXT文件
    try:
        with open(input_file, 'r', encoding=input_encoding) as txt_file:
            lines = txt_file.readlines()
    except UnicodeDecodeError:
        # 如果尝试的编码失败，尝试使用其他常见编码
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            if enc != input_encoding:
                try:
                    with open(input_file, 'r', encoding=enc) as txt_file:
                        lines = txt_file.readlines()
                    input_encoding = enc  # 更新成功的编码
                    break
                except UnicodeDecodeError:
                    continue
        else:
            raise Exception("无法识别文件编码，请尝试指定正确的编码")
    
    processed_lines = []
    
    # 处理每一行
    for line in lines:
        line = line.strip()
        if line:  # 跳过空行
            fields = line.split(delimiter)
            processed_lines.append(fields)
    
    # 写入CSV文件
    with open(output_file, 'w', encoding=output_encoding, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(processed_lines)
    
    return len(processed_lines)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
