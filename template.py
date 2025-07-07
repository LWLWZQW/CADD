import math
import csv
import matplotlib.pyplot as plt

def LeakyRELU(X, alpha):
    Y = []
    for x in X:
        if x >= 0:
            Y.append(x)
        else:
            Y.append(alpha * x)
    return Y 
print(LeakyRELU([-4, -2, 2, 4],0.1))

def encode_dna_sequence(input):
    # Define the one-hot encoding mapping for each nucleotide
    encoding = {
        'G': [1, 0, 0, 0],
        'C': [0, 1, 0, 0],
        'T': [0, 0, 1, 0],
        'A': [0, 0, 0, 1]
    }
    # Initialize an empty list to store the encoded rows
    encoded_sequence = []
    # Iterate over each character in the input sequence
    for nucleotide in input:
        # Get the one-hot encoded vector for the current nucleotide
        encoded_vector = encoding.get(nucleotide, [0, 0, 0, 0])  # Default to [0,0,0,0] if invalid (though input should only be G,C,T,A)
        encoded_sequence.append(encoded_vector)
    
    return encoded_sequence
print(encode_dna_sequence("ATCGTTT")) 

def max_pooling(X, pool_size):
    rows = len(X)
    cols = len(X[0]) if rows > 0 else 0
    
    out_rows = rows // pool_size
    out_cols = cols // pool_size
    
    Y = []
    
    for i in range(out_rows):
        for j in range(out_cols):
            window = [
                X[i*pool_size + di][j*pool_size + dj]
                for di in range(pool_size)
                for dj in range(pool_size)
            ]
            Y.append(max(window))
    
    return [Y] 
print(max_pooling([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 2))



def sinusoidal_regression(x_vals, y_vals, max_iter=5000, lr=0.01, tolerance=1e-5):
    a = (max(y_vals) - min(y_vals)) / 2  # 振幅
    b = 2 * math.pi * 2 / (max(x_vals) - min(x_vals))  # 假设2个周期
    c = 0.0  # 初始相位
    n = len(x_vals)
    prev_loss = float('inf')
    a, b, c = 2, 1.5, 0.0  # 手动初始化
    n = len(x_vals)
    prev_loss = float('inf')
    
    for epoch in range(max_iter):
        grad_a, grad_b, grad_c = 0, 0, 0
        current_loss = 0
        
        for x, y in zip(x_vals, y_vals):
            sin_term = math.sin(b * x + c)
            error = a * sin_term - y
            grad_a += error * sin_term
            grad_b += error * a * x * math.cos(b * x + c)
            grad_c += error * a * math.cos(b * x + c)
            current_loss += error ** 2
        
        # 梯度裁剪（限制梯度范围）
        max_grad = 1.0
        grad_a = max(min(grad_a, max_grad), -max_grad)
        grad_b = max(min(grad_b, max_grad), -max_grad)
        grad_c = max(min(grad_c, max_grad), -max_grad)
        
        # 更新参数
        a -= (lr / n) * grad_a
        b -= (lr / n) * grad_b
        c -= (lr / n) * grad_c
        
        # 早停
        current_loss /= n
        if abs(prev_loss - current_loss) < tolerance:
            break
        prev_loss = current_loss
    
    return float(a), float(b), float(c)



def main():
    print("While you may use the main() function to test your own code,")
    print("none of its contents will be run or marked.")
    print("Also, anything printed to the console won't be marked")
    print("We will only mark your function definitions by importing your code as a module.")
    print(LeakyRELU([-4, -2, 2, 4],0.1))
    print(encode_dna_sequence("ATCGTTT"))
    print(max_pooling([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],2))

    file_name = "q4data.csv"

    # Load data from the file
    x_vals, y_vals = [], []
    with open(file_name, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_vals.append(float(row["x"]))
            y_vals.append(float(row["y"]))

    a, b, c = sinusoidal_regression(x_vals, y_vals)

    def predict(a, b, c, x_list):
        return [a * math.sin(b * x + c) for x in x_list]

    y_pred = predict(a, b, c, x_vals)

    plt.figure()
    plt.plot(x_vals, y_vals, 'ro', label='Original data')
    plt.plot(x_vals, y_pred, 'b-', label='Best fit')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()


