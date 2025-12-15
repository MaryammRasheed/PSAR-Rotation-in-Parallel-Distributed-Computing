import multiprocessing
import tkinter as tk
import time
import math

# ---------------- PSAR PREFIX PROCESS ----------------
def psar_prefix_process(pid, in_q, out_q, gui_q, rounds):
    value = pid + 1        # initial value
    prefix_sum = value

    for r in range(rounds):
        out_q.put(prefix_sum)
        received = in_q.get()
        prefix_sum += received

        gui_q.put((pid, prefix_sum, r + 1))
        time.sleep(1)

# ---------------- PARALLEL EXECUTION ----------------
def start_psar(gui_q):
    n = 5
    rounds = n - 1

    queues = [multiprocessing.Queue() for _ in range(n)]
    processes = []

    for i in range(n):
        p = multiprocessing.Process(
            target=psar_prefix_process,
            args=(
                i,
                queues[i],
                queues[(i + 1) % n],
                gui_q,
                rounds
            )
        )
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    gui_q.put("DONE")

# ---------------- GUI ----------------
def update_gui():
    while not gui_queue.empty():
        msg = gui_queue.get()

        if msg == "DONE":
            log.insert(tk.END, "\n✔ Prefix-Sum Completed\n")
            return

        pid, prefix, rnd = msg
        log.insert(tk.END, f"Process {pid} | Round {rnd} | Prefix Sum = {prefix}\n")
        log.see(tk.END)

        update_ring(pid, prefix)

    root.after(300, update_gui)

def update_ring(active_pid, value):
    canvas.delete("all")
    radius = 130
    center_x, center_y = 200, 170
    nodes = 5

    for i in range(nodes):
        angle = (2 * math.pi / nodes) * i
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        color = "green" if i == active_pid else "skyblue"
        canvas.create_oval(x-25, y-25, x+25, y+25, fill=color)
        canvas.create_text(x, y, text=f"P{i}")

    canvas.create_text(
        center_x, center_y,
        text=f"Value = {value}",
        font=("Arial", 12, "bold")
    )

def run_psar():
    start_btn.config(state=tk.DISABLED)
    multiprocessing.Process(target=start_psar, args=(gui_queue,)).start()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    multiprocessing.freeze_support()

    root = tk.Tk()
    root.title("Animated PSAR Prefix-Sum")
    root.geometry("700x520")

    tk.Label(
        root,
        text="PSAR Prefix-Sum (Animated Ring)",
        font=("Arial", 16, "bold")
    ).pack(pady=5)

    canvas = tk.Canvas(root, width=400, height=350, bg="white")
    canvas.pack()

    log = tk.Text(root, width=80, height=8)
    log.pack(pady=5)

    start_btn = tk.Button(
        root,
        text="Start Prefix-Sum PSAR",
        font=("Arial", 12),
        command=run_psar
    )
    start_btn.pack(pady=5)

    gui_queue = multiprocessing.Queue()

    root.after(300, update_gui)
    root.mainloop()
