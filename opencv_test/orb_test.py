import cv2
import numpy as np

query_img = cv2.imread('skip_button.png')  # 查询图像
train_img = cv2.imread('skip_button.png')  # 训练图像
query_img_bw = cv2.cvtColor(query_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
train_img_bw = cv2.cvtColor(train_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
orb = cv2.ORB.create(edgeThreshold=0)  # 初始化ORB检测器
queryKeypoints, queryDescriptors = orb.detectAndCompute(query_img_bw, None)  # 在查询图像中找到关键点和描述符
trainKeypoints, trainDescriptors = orb.detectAndCompute(train_img_bw, None)  # 在训练图像中找到关键点和描述符
print("queryDescriptors shape:", queryDescriptors.shape)  # 打印查询图像的描述符的形状
print("trainDescriptors shape:", trainDescriptors.shape)  # 打印训练图像的描述符的形状
queryDescriptors = queryDescriptors.astype(np.float32)  # 转换查询图像的描述符的数据类型为浮点数
trainDescriptors = trainDescriptors.astype(np.float32)  # 转换训练图像的描述符的数据类型为浮点数
matcher = cv2.BFMatcher()  # 创建暴力匹配器
matches = matcher.match(queryDescriptors, trainDescriptors)  # 匹配两组描述符
final_img = cv2.drawMatches(query_img, queryKeypoints, train_img, trainKeypoints, matches[:20], None)  # 绘制前20个最佳匹配
final_img = cv2.resize(final_img, (1000, 650))  # 调整图像大小
cv2.imshow("Matches", final_img)  # 显示匹配结果
cv2.waitKey(3000)  # 等待3秒
