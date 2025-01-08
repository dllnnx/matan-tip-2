import numpy as np
import time

analytical_value = 16 / 3   # значение интеграла, полученное на аналитическом этапе


# D: x^2 + y^2 <= 4, y >= 0
def is_in_D(x, y):
    return x**2 + y**2 <= 4 and y >= 0


def parametrize_circle(delta):
    t_values = np.arange(0, np.pi + delta, delta)[::-1]
    peaks = [(-2, 0)]
    peaks += [(2 * np.cos(t), 2 * np.sin(t)) for t in t_values]  # peaks - вершины вписанной ломаной
    return peaks


# расчет интеграла напрямую
def compute_line_integral(peaks):
    integral_sum = 0
    for i in range(len(peaks)):
        x1, y1 = peaks[i]
        x2, y2 = peaks[i - 1]
        dx = x2 - x1
        dy = y2 - y1

        f = (x1**2 + y1**2)
        g = x1 * y1

        integral_sum += f * dx + g * dy

    return integral_sum


# расчет по формуле Грина
def compute_double_integral(delta):
    x_values = np.arange(-2, 2 + delta, delta)
    y_values = np.arange(0, 2 + delta, delta)

    integral_sum = 0
    for x in x_values:
        for y in y_values:
            if is_in_D(x, y):
                f = -y
                integral_sum += f * delta**2

    return -integral_sum  # минус чтобы учесть направление обхода


results_line_integral = []
results_double_integral = []

for delta in [0.1, 0.01, 0.001]:
    start_time = time.time()
    peaks = parametrize_circle(delta)
    line_integral_sum = compute_line_integral(peaks)
    end_time = time.time()

    results_line_integral.append({
        "delta": delta,
        "integral_sum": line_integral_sum,
        "deviation": abs(line_integral_sum - analytical_value),
        "time": end_time - start_time
    })

    start_time = time.time()
    double_integral_sum = compute_double_integral(delta)
    end_time = time.time()

    results_double_integral.append({
        "delta": delta,
        "integral_sum": double_integral_sum,
        "deviation": abs(double_integral_sum - analytical_value),
        "time": end_time - start_time
    })

print(f"Истинное значение: {analytical_value:.6f}")
print("\nКриволинейный интеграл:")
print("delta | integral sum | deviation | time (s)")
for res in results_line_integral:
    print(f"{res['delta']:.3f} | {res['integral_sum']:12.6f} | {res['deviation']:9.6f} | {res['time']:.6f}")

print("\nДвойной интеграл:")
print("delta | integral sum | deviation | time (s)")
for res in results_double_integral:
    print(f"{res['delta']:.3f} | {res['integral_sum']:12.6f} | {res['deviation']:9.6f} | {res['time']:.6f}")
