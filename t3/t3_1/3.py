import torch
import torch.nn as nn
import torch.optim as optim # 导入优化器模块
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# --- Hyperparameters and Configuration ---
BATCH_SIZE = 128
NUM_WORKERS = 2
DATA_ROOT = './data'
# Determine the device to use for training (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# --- Data Preprocessing ---
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# --- Data Loading Function ---
def load_cifar10_data(root, batch_size, num_workers, transform):
    """
    Loads CIFAR-10 train and test datasets and creates PyTorch DataLoaders.
    加载 CIFAR-10 训练集和测试集，并创建 PyTorch DataLoaders。
    """
    print(f"尝试从 {root} 加载 CIFAR-10 数据")
    trainset = torchvision.datasets.CIFAR10(
        root=root, train=True, download=True, transform=transform
    )
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )
    testset = torchvision.datasets.CIFAR10(
        root=root, train=False, download=True, transform=transform
    )
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )
    classes = trainset.classes
    print("数据加载成功!")
    print(f"训练样本数量: {len(trainset)}")
    print(f"测试样本数量: {len(testset)}")
    return trainloader, testloader, classes

# --- MLP Model Definition ---
class MLP(nn.Module):
    def __init__(self, input_size, num_classes):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, 512)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(512, 256)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

# --- Main Execution Block ---
if __name__ == "__main__":
    # Load the data
    trainloader, testloader, classes = load_cifar10_data(
        root=DATA_ROOT,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        transform=transform
    )

    # Define model parameters
    input_size = 3 * 32 * 32
    num_classes = 10

    # Instantiate the model and move it to the device
    model = MLP(input_size, num_classes).to(device)
    print("\nMLP model created:")
    print(model)

    # --- Training Settings ---
    # Define the loss function - CrossEntropyLoss is suitable for multi-class classification
    # 定义损失函数 - CrossEntropyLoss 适用于多类别分类问题
    criterion = nn.CrossEntropyLoss()
    # Define the optimizer - Use Adam optimizer
    # 定义优化器 - 使用 Adam 优化器
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Define the total number of training epochs
    # 定义训练的总轮数 (epochs)
    num_epochs = 20 # You can adjust this number

    # Store training loss and test accuracy for potential visualization (Optional)
    # 存储训练过程中的损失和测试准确率，以便后续可视化 (可选)
    train_losses = []
    test_accuracies = []

    # --- Training Loop ---
    print("\nStarting training...")
    for epoch in range(num_epochs):
        # Set the model to training mode
        # 设置模型为训练模式 (启用 Dropout/BatchNorm 等)
        model.train()
        running_loss = 0.0
        # Iterate over batches from the training data loader
        # 遍历训练数据加载器中的批次
        for i, data in enumerate(trainloader, 0):
            # Get the inputs and labels for the current batch
            # 获取一个批次的输入图像和对应的标签
            inputs, labels = data
            # Move data to the specified device (CPU/GPU)
            # 将数据移动到指定的设备 (CPU/GPU)
            inputs, labels = inputs.to(device), labels.to(device)

            # Zero the gradients
            # 在进行反向传播之前，需要将模型参数的梯度缓冲区清零
            optimizer.zero_grad()

            # Forward pass
            # 通过模型获取预测输出
            outputs = model(inputs)
            # Calculate the loss between predicted outputs and true labels
            # 计算预测输出与真实标签之间的损失
            loss = criterion(outputs, labels)

            # Backward pass
            # 根据损失计算每个参数的梯度
            loss.backward()
            # Optimizer step - update model parameters based on gradients
            # 优化器更新模型参数
            optimizer.step()

            # Accumulate and print training loss
            # 统计并打印训练损失
            running_loss += loss.item()
            # Print statistics every 100 batches
            # 每 100 个批次打印一次平均损失
            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(trainloader)}], Loss: {running_loss / 100:.4f}')
                train_losses.append(running_loss / 100)
                running_loss = 0.0

        # --- Test/Evaluation Loop (after each Epoch) ---
        # Set the model to evaluation mode
        # 设置模型为评估模式 (关闭 Dropout，使用 BatchNorm 的全局统计信息等)
        model.eval()
        correct = 0
        total = 0
        # Disable gradient calculation during evaluation
        # 在评估阶段，不需要计算梯度，使用 torch.no_grad() 可以节省内存和计算
        with torch.no_grad():
            # Iterate over batches from the test data loader
            # 遍历测试数据加载器中的批次
            for data in testloader:
                images, labels = data
                # Move data to the device
                # 将数据移动到指定的设备
                images, labels = images.to(device), labels.to(device)
                # Forward pass
                # 前向传播
                outputs = model(images)
                # Get the predicted class (index of the highest score) for each sample
                # 获取每个样本预测的最高得分及其对应的类别索引
                # outputs.data is (batch_size, num_classes), torch.max finds max along dimension 1
                _, predicted = torch.max(outputs.data, 1)
                # Accumulate total number of samples
                # 累加总样本数
                total += labels.size(0)
                # Accumulate number of correctly predicted samples
                # 累加预测正确的样本数
                correct += (predicted == labels).sum().item()

        # Calculate and print the test accuracy for the current epoch
        # 计算并打印当前 Epoch 的测试准确率
        epoch_accuracy = 100 * correct / total
        test_accuracies.append(epoch_accuracy)
        print(f'Epoch [{epoch + 1}/{num_epochs}], Test Accuracy: {epoch_accuracy:.2f} %')

    print('Finished Training')

    # --- Final Model Evaluation (Optional, but good practice) ---
    # This part is already included in the training loop, but you can run it again
    # after training is finished for a final report.
    # 最终模型评估 (可选，但推荐)
    # 这部分代码已经包含在训练循环中，但你可以在训练结束后再次运行，以获取最终报告。
    print("\nStarting final evaluation...")
    model.eval() # Ensure in evaluation mode
    correct = 0
    total = 0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))

    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            c = (predicted == labels).squeeze()
            for i in range(labels.size(0)):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    overall_accuracy = 100 * correct / total
    print(f'Accuracy of the network on the {total} test images: {overall_accuracy:.2f} %')

    print('\nAccuracy for each class:')
    for i in range(10):
        if class_total[i] > 0:
            print(f'Accuracy of {classes[i]:5s} : {100 * class_correct[i] / class_total[i]:.2f} %')
        else:
            print(f'Accuracy of {classes[i]:5s} : N/A') # Should not happen for CIFAR-10


    # --- Visualize Training Progress (Optional) ---
    # If you want to see the curves of training loss and test accuracy, uncomment the following block
    # 如果你想看到训练损失和测试准确率的曲线，取消下面的注释并运行
    # try:
    #     plt.figure(figsize=(10, 4))
    #     plt.subplot(1, 2, 1)
    #     plt.plot(train_losses)
    #     plt.title('Training Loss per 100 Batches')
    #     plt.xlabel('Batch (x100)')
    #     plt.ylabel('Loss')
    #
    #     plt.subplot(1, 2, 2)
    #     plt.plot(range(1, num_epochs + 1), test_accuracies)
    #     plt.title('Test Accuracy per Epoch')
    #     plt.xlabel('Epoch')
    #     plt.ylabel('Accuracy (%)')
    #
    #     plt.tight_layout()
    #     plt.show()
    # except Exception as e:
    #      print(f"\nCould not plot training progress: {e}")
    #      print("Please ensure matplotlib is installed.")
