import urllib.parse
import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Định nghĩa mật khẩu MongoDB Atlas
db_password = 'Kaidotuhoang1@'  # Thay bằng mật khẩu thực tế của bạn

# Mã hóa tên người dùng và mật khẩu
username = urllib.parse.quote_plus('lcthinh286')
password = urllib.parse.quote_plus(db_password)

# URI kết nối MongoDB Atlas
uri = f"mongodb+srv://{username}:{password}@cluster0.upmr8jn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Kết nối với MongoDB
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    logger.info("Kết nối thành công với MongoDB Atlas!")
except Exception as e:
    logger.error(f"Lỗi kết nối MongoDB: {e}")
    raise

# Chọn database và collection
db = client["phishing_db"]
models_collection = db["models"]

# Tải tập dữ liệu
try:
    data = pd.read_csv('phishing_dataset.csv')
    logger.info("Tải tệp phishing_dataset.csv thành công")
except FileNotFoundError:
    logger.error("Không tìm thấy tệp phishing_dataset.csv")
    raise
except Exception as e:
    logger.error(f"Lỗi khi tải tệp CSV: {e}")
    raise

# Kiểm tra tên cột
logger.info(f"Tên cột trong dữ liệu: {list(data.columns)}")

# Kiểm tra sự tồn tại của cột 'id' và 'Result'
required_columns = ['id', 'Result']
for col in required_columns:
    if col not in data.columns:
        logger.error(f"Cột '{col}' không tồn tại trong dữ liệu")
        raise ValueError(f"Cột '{col}' không tồn tại trong dữ liệu")

# Chuẩn bị dữ liệu huấn luyện
try:
    X = data.drop(['id', 'Result'], axis=1)
    y = data['Result']
    logger.info("Chuẩn bị dữ liệu huấn luyện thành công")
except Exception as e:
    logger.error(f"Lỗi khi chuẩn bị dữ liệu: {e}")
    raise

# Huấn luyện mô hình
try:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    logger.info("Huấn luyện mô hình RandomForestClassifier thành công")
except Exception as e:
    logger.error(f"Lỗi khi huấn luyện mô hình: {e}")
    raise

# Serialize mô hình
def serialize_tree(tree):
    tree_ = tree.tree_
    def recurse(node):
        if tree_.feature[node] != -2:
            return {
                "feature": int(tree_.feature[node]),
                "threshold": float(tree_.threshold[node]),
                "left": recurse(tree_.children_left[node]),
                "right": recurse(tree_.children_right[node])
            }
        else:
            return {"value": tree_.value[node].tolist()}
    return recurse(0)

try:
    forest = [serialize_tree(est) for est in clf.estimators_]
    logger.info("Serialize mô hình thành công")
except Exception as e:
    logger.error(f"Lỗi khi serialize mô hình: {e}")
    raise

# Lưu mô hình vào MongoDB
try:
    model_doc = {"_id": "current_model", "data": forest}
    models_collection.replace_one({"_id": "current_model"}, model_doc, upsert=True)
    logger.info("Lưu mô hình vào MongoDB thành công")
except Exception as e:
    logger.error(f"Lỗi khi lưu mô hình vào MongoDB: {e}")
    raise

# Đóng kết nối
try:
    client.close()
    logger.info("Đóng kết nối MongoDB thành công")
except Exception as e:
    logger.error(f"Lỗi khi đóng kết nối MongoDB: {e}")