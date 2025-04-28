import torch
import torch.nn as nn

# 设置设备 - 如果有GPU，使用GPU
# This line needs to be executed BEFORE you use the 'device' variable
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# MLP 模型定义
class MLP(nn.Module):
    def __init__(self, input_size, num_classes):
        super(MLP, self).__init__()
        # 第一个全连接层: 输入层大小 -> 隐藏层 1 神经元数
        self.fc1 = nn.Linear(input_size, 512)
        # ReLU 激活函数
        self.relu1 = nn.ReLU()
        # 第二个全连接层: 隐藏层 1 神经元数 -> 隐藏层 2 神经元数
        self.fc2 = nn.Linear(512, 256)
        # ReLU 激活函数
        self.relu2 = nn.ReLU()
        # 输出层: 隐藏层 2 神经元数 -> 输出类别数
        # CrossEntropyLoss 包含了 Softmax，所以输出层不需要激活函数
        self.fc3 = nn.Linear(256, num_classes)

    def forward(self, x):
        # MLP 需要将图像展平
        # x.size(0) 是批量大小，-1 会自动计算剩余维度的大小 (3 * 32 * 32 = 3072)
        x = x.view(x.size(0), -1)

        # 前向传播通过各层和激活函数
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x) # 输出层

        return x

# 定义模型参数
# CIFAR-10 图像大小 3x32x32，展平后输入大小为 3 * 32 * 32 = 3072
input_size = 3 * 32 * 32
# CIFAR-10 有 10 个类别
num_classes = 10

# 实例化模型并将其移动到之前检测到的设备 (CPU 或 GPU)
model = MLP(input_size, num_classes).to(device)

print("\nMLP model created:")
print(model)
