import torch
import torch.nn as nn # 导入神经网络模块，后续构建模型需要
import torch.optim as optim # 导入优化器模块，后续训练模型需要
import torchvision # 导入 torchvision 库，用于处理视觉数据（数据集、模型、变换等）
import torchvision.transforms as transforms # 导入图像变换模块
import matplotlib.pyplot as plt # 导入 matplotlib 库，用于绘图（可选，用于可视化）
import numpy as np # 导入 numpy 库，用于数值计算（可选）

# --- 超参数和配置 ---
# 定义数据加载器的批量大小 (Batch Size)
BATCH_SIZE = 128
# 定义数据加载的工作进程数 (Number of Worker Threads)
# 根据你的 CPU 核心数进行调整。
# 更多的工作进程可以加快数据加载速度，但过多可能会消耗过多资源。
NUM_WORKERS = 2
# 定义数据集下载和存储的目录
DATA_ROOT = './data'
# 确定用于训练的设备 (如果 GPU 可用，则使用 GPU，否则使用 CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# --- 数据预处理 ---
# 定义图像的变换序列
# transforms.Compose 将多个变换按顺序组合
transform = transforms.Compose([
    # 1. transforms.ToTensor(): 将 PIL Image 或 numpy.ndarray 转换为 Tensor。
    #    将像素值从 [0, 255] 缩放到 [0.0, 1.0]。
    transforms.ToTensor(),
    # 2. transforms.Normalize(): 使用均值和标准差对 Tensor 进行归一化。
    #    这些是 CIFAR-10 数据集计算得出的标准均值和标准差。
    #    公式: output[channel] = (input[channel] - mean[channel]) / std[channel]
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# --- 数据加载函数 ---
def load_cifar10_data(root, batch_size, num_workers, transform):
    """
    加载 CIFAR-10 训练集和测试集，并创建 PyTorch DataLoaders。

    Args:
        root (str): 数据集下载和存储的目录。
        batch_size (int): 每个批次的样本数量。
        num_workers (int): 数据加载的子进程数量。
        transform (torchvision.transforms.Compose): 应用于图像的变换。

    Returns:
        tuple: 包含以下元素的元组：
            - trainloader (torch.utils.data.DataLoader): 训练集的 DataLoader。
            - testloader (torch.utils.data.DataLoader): 测试集的 DataLoader。
            - classes (tuple): 类别名称的元组。
    """
    print(f"尝试从 {root} 加载 CIFAR-10 数据")

    # 加载训练集
    # download=True: 如果在 root 目录中找不到数据集，则会下载数据集
    trainset = torchvision.datasets.CIFAR10(
        root=root,
        train=True, # 指定加载训练集
        download=True, # 如果本地没有则下载 (第一次运行设为 True，之后可设为 False)
        transform=transform # 应用上面定义的图像变换
    )
    # 创建训练集的 DataLoader
    # shuffle=True: 在每个 epoch 开始时打乱数据顺序，这对于训练至关重要
    # pin_memory=True: 如果使用 GPU，可以加速数据从 CPU 到 GPU 的传输
    trainloader = torch.utils.data.DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )

    # 加载测试集
    testset = torchvision.datasets.CIFAR10(
        root=root,
        train=False, # 指定加载测试集
        download=True, # 如果本地没有则下载 (第一次运行设为 True，之后可设为 False)
        transform=transform # 应用上面定义的图像变换
    )
    # 创建测试集的 DataLoader
    # shuffle=False: 对于测试/评估，数据顺序通常不重要，不打乱
    # pin_memory=True: 如果使用 GPU，可以加速数据从 CPU 到 GPU 的传输
    testloader = torch.utils.data.DataLoader(
        testset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )

    # 从数据集对象中获取类别名称
    classes = trainset.classes

    print("数据加载成功!")
    print(f"训练样本数量: {len(trainset)}")
    print(f"测试样本数量: {len(testset)}")

    return trainloader, testloader, classes

# --- 主执行块 ---
# 这个块只在直接运行这个脚本时执行 (而不是作为模块被导入时)
if __name__ == "__main__":
    # 使用定义的函数和参数加载数据
    trainloader, testloader, classes = load_cifar10_data(
        root=DATA_ROOT,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        transform=transform
    )

    # 可选: 通过查看一个批次的数据来验证是否正确加载 (取消下面的注释并运行)
    # try:
    #     # 获取一个随机批次的训练图像和标签
    #     dataiter = iter(trainloader)
    #     images, labels = next(dataiter)
    #
    #     print("\n样本批次形状:")
    #     print("图像形状:", images.shape) # 形状应该是 [BATCH_SIZE, 3, 32, 32]
    #     print("标签形状:", labels.shape) # 形状应该是 [BATCH_SIZE]
    #
    #     # 打印前几个标签及其对应的类别名称
    #     print("样本标签:", labels[:8])
    #     print("对应的类别:", [classes[label] for label in labels[:8]])
    #
    #     # # 可选: 显示一些图像 (需要安装 matplotlib)
    #     # def imshow(img):
    #     #     # 反归一化图像 (如果使用了提供的均值/标准差，这是一个近似值)
    #     #     img = img / 2 + 0.5
    #     #     npimg = img.numpy()
    #     #     # 将 Tensor 的形状 (C, H, W) 转换为 numpy 的形状 (H, W, C) 以便显示
    #     #     plt.imshow(np.transpose(npimg, (1, 2, 0)))
    #     #     plt.show()
    #     #
    #     # print('显示样本图像:')
    #     # # 显示批次中的前 8 张图像
    #     # imshow(torchvision.utils.make_grid(images[:8]))
    #
    # except Exception as e:
    #      print(f"无法获取样本批次: {e}")
    #      print("这可能发生在数据加载失败后。")


    print("\n数据加载阶段完成。现在可以继续定义你的 MLP 模型、损失函数、优化器和训练循环了。")
