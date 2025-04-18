import os
import torch
import time

# 防止OpenMP库冲突（针对CPU版）
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # [2](@ref)

def test_pytorch_environment():
    # 基础环境验证
    print(f"PyTorch版本: {torch.__version__}")  # [1,2](@ref)
    print(f"CUDA是否可用: {torch.cuda.is_available()}")  # [1,5](@ref)

    # 设备检测逻辑
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"当前运行设备: {device}")

    # 张量计算测试
    test_tensor_operations(device)

    # 神经网络层测试
    test_neural_network()

    # 性能基准测试
    run_performance_benchmark(device)

def test_tensor_operations(device):
    # 基本张量运算
    x = torch.randn(3, 3).to(device)
    y = torch.randn(3, 3).to(device)
    z = x @ y  # 矩阵乘法
    print(f"\n张量运算结果示例:\n{z}")  # [1](@ref)

    # 类型转换测试
    int_tensor = torch.tensor([1, 2, 3], dtype=torch.int32)
    float_tensor = int_tensor.float()
    print(f"\n类型转换测试: {float_tensor.dtype}")

def test_neural_network():
    # 简单神经网络测试
    model = torch.nn.Sequential(
        torch.nn.Linear(10, 5),
        torch.nn.ReLU(),
        torch.nn.Linear(5, 2)
    )
    input_data = torch.randn(1, 10)
    output = model(input_data)
    print(f"\n神经网络输出维度: {output.shape}")  # [1,5](@ref)

def run_performance_benchmark(device):
    # 性能基准测试（适合CPU/GPU）
    matrix_size = 1000
    a = torch.randn(matrix_size, matrix_size).to(device)
    b = torch.randn(matrix_size, matrix_size).to(device)

    # 预热GPU（如果有）
    if device.type == 'cuda':
        _ = a @ b  # [5](@ref)
        torch.cuda.synchronize()

    # 计时测试
    start_time = time.time()
    for _ in range(10):
        _ = a @ b
    if device.type == 'cuda':
        torch.cuda.synchronize()
    elapsed = (time.time() - start_time) * 1000  # 毫秒
    print(f"\n矩阵乘法性能（{matrix_size}x{matrix_size}）: {elapsed:.2f}ms")

if __name__ == "__main__":
    test_pytorch_environment()