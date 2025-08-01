---
title: "Reinforcement Learning: Học Tăng Cường từ Lý thuyết đến Thực hành"
date: "2025-01-27"
author: "Huy Hiep Nguyen"
category: "til"
tags: ["reinforcement learning", "rl", "q-learning", "dqn", "ppo", "openai gym", "stable baselines3", "machine learning", "python"]
excerpt: "Hướng dẫn chuyên sâu về Reinforcement Learning - từ khái niệm cơ bản đến các thuật toán Q-learning, DQN, PPO với ví dụ code thực tế sử dụng OpenAI Gym."
featured: false
---

# Reinforcement Learning: Học Tăng Cường từ Lý thuyết đến Thực hành

Bạn đã từng tự hỏi làm thế nào mà các siêu AI có thể đánh bại kiện tướng cờ vây, điều khiển robot hay tự động lái xe? Câu trả lời nằm ở **Học Tăng Cường (Reinforcement Learning - RL)**. Khác với học có giám sát (supervised learning) chỉ học từ các ví dụ được gán nhãn sẵn, RL học thông qua quá trình thử và sai, nhận phần thưởng hoặc hình phạt từ môi trường.

Bài viết này sẽ đưa bạn đi từ những khái niệm cốt lõi đến các thuật toán cơ bản, cùng với ví dụ minh họa bằng code để giúp bạn bắt đầu một cách bài bản.

## **1. Các Khái niệm Cơ bản của Học Tăng cường**

Hãy tưởng tượng bạn đang huấn luyện một chú chó. Quá trình đó chính là RL.

* **Agent (Tác nhân):** Chú chó - thực thể đưa ra hành động. Trong ML, agent là mô hình mà chúng ta huấn luyện.
* **Environment (Môi trường):** Thế giới xung quanh chú chó - nơi nó tương tác.
* **State (Trạng thái):** Tình huống hiện tại của môi trường. Ví dụ: Chú chó đang ngồi.
* **Action (Hành động):** Các lựa chọn mà agent có thể thực hiện. Ví dụ: Chú chó ngồi xuống, đứng lên, sủa.
* **Reward (Phần thưởng):** Phản hồi từ môi trường cho mỗi hành động. Phần thưởng có thể là dương (cho chú chó một miếng bánh khi ngồi) hoặc âm (la rầy khi sủa bậy). Mục tiêu của agent là tối đa hóa tổng phần thưởng nhận được theo thời gian.

Quy trình diễn ra như sau: Agent quan sát **trạng thái** hiện tại, thực hiện một **hành động**, môi trường chuyển sang **trạng thái** mới và trả về một **phần thưởng**. Vòng lặp này cứ tiếp diễn cho đến khi kết thúc một "vòng chơi" (episode).

## **2. Các Thuật toán RL Cơ bản**

Các thuật toán RL được chia thành ba nhóm chính, mỗi nhóm có cách tiếp cận khác nhau để giải quyết bài toán.

### **a. Thuật toán Dựa trên Giá trị (Value-based)**

Các thuật toán này học một hàm giá trị để ước tính mức độ "tốt" của một trạng thái hoặc một cặp trạng thái-hành động. Agent sau đó chọn hành động có giá trị cao nhất.

* **Q-learning:** Một trong những thuật toán RL kinh điển. Nó học một bảng Q (Q-table), trong đó mỗi ô `Q(state, action)` chứa giá trị ước tính cho việc thực hiện một hành động cụ thể ở một trạng thái nhất định.

  * **Thách thức:** Bảng Q trở nên quá lớn khi không gian trạng thái và hành động mở rộng.

* **Deep Q Network (DQN):** Một bước đột phá, kết hợp Q-learning với học sâu (Deep Learning). Thay vì sử dụng bảng, DQN sử dụng một mạng nơ-ron để xấp xỉ hàm Q, giúp giải quyết các bài toán có không gian trạng thái cực lớn.

### **b. Thuật toán Dựa trên Chính sách (Policy-based)**

Các thuật toán này học trực tiếp một chính sách (policy) - ánh xạ từ trạng thái đến hành động. Chính sách có thể là một hàm xác suất, cho biết xác suất thực hiện mỗi hành động ở một trạng thái cụ thể.

* **REINFORCE:** Một thuật toán dựa trên gradient, sử dụng đạo hàm để cập nhật chính sách. Mục tiêu là tăng xác suất của các hành động mang lại phần thưởng cao và giảm xác suất của các hành động mang lại phần thưởng thấp.

### **c. Phương pháp Actor-Critic**

Kết hợp ưu điểm của cả hai loại trên.

* **Actor:** Một mạng nơ-ron học chính sách (policy-based) để quyết định hành động nào sẽ được thực hiện.
* **Critic:** Một mạng nơ-ron học hàm giá trị (value-based) để đánh giá hành động của actor.

Critic sẽ cung cấp phản hồi cho actor, giúp actor học chính sách tốt hơn. Đây là nền tảng của nhiều thuật toán RL hiện đại.

## **3. Minh họa với OpenAI Gym và Code Python**

**OpenAI Gym** là một thư viện tuyệt vời để thử nghiệm các thuật toán RL. Chúng ta sẽ sử dụng môi trường `CartPole-v1` và thư viện **Stable Baselines3** để huấn luyện một agent đơn giản.

```python
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# 1. Tạo môi trường
# CartPole-v1: Mục tiêu là giữ một cây sào thẳng đứng trên một toa xe di chuyển.
env_id = "CartPole-v1"
env = make_vec_env(env_id, n_envs=1)

# 2. Chọn và huấn luyện thuật toán
# PPO (Proximal Policy Optimization) là một thuật toán Actor-Critic hiệu quả.
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# 3. Kiểm tra agent đã huấn luyện
print("Bắt đầu kiểm tra agent đã học:")
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    env.render()
    if dones:
        print("Agent đã hoàn thành một vòng chơi!")
        break

env.close()
```

**Giải thích code:**

* **`make_vec_env`:** Tạo môi trường CartPole, nơi agent sẽ học cách cân bằng cây sào.
* **`PPO("MlpPolicy", env)`:** Khởi tạo mô hình PPO với một chính sách dạng mạng nơ-ron nhiều lớp (MlpPolicy).
* **`model.learn()`:** Huấn luyện mô hình trong 10.000 bước. Trong quá trình này, agent sẽ thử và sai, nhận phần thưởng (khi cây sào được giữ thẳng) và cập nhật chính sách của mình.
* **`model.predict()`:** Sử dụng mô hình đã huấn luyện để đưa ra hành động dự đoán.

## **4. Thách thức và Ứng dụng Thực tế**

### **a. Thách thức**

* **Exploration vs. Exploitation (Khám phá vs. Khai thác):** Agent cần phải cân bằng giữa việc khám phá các hành động mới để tìm ra chiến lược tốt hơn và khai thác các hành động đã biết để nhận phần thưởng cao.
* **Sample Efficiency:** RL thường đòi hỏi một lượng lớn dữ liệu tương tác để học, điều này có thể rất tốn kém trong các môi trường thực tế như robot.
* **Stability:** Việc huấn luyện mạng nơ-ron trong RL có thể không ổn định, dễ bị phân kỳ.

### **b. Ứng dụng Thực tế**

* **Game AI:** Nổi tiếng nhất là các hệ thống AI chơi game Atari, cờ vây (AlphaGo) và cờ vua, vượt trội hơn cả con người.
* **Robot và Tự động hóa:** Huấn luyện robot thực hiện các nhiệm vụ phức tạp như gắp đồ vật, đi lại.
* **Hệ thống Khuyến nghị:** Các nền tảng như Netflix, Spotify sử dụng RL để tối ưu hóa việc đề xuất nội dung, tối đa hóa thời gian người dùng tương tác.
* **Tối ưu hóa Vận hành:** Tối ưu hóa chuỗi cung ứng, điều khiển giao thông, quản lý tài nguyên trong các trung tâm dữ liệu.

## **Kết luận**

Học Tăng Cường là một lĩnh vực đầy tiềm năng, mở ra khả năng tạo ra các hệ thống AI có khả năng tự học và thích nghi. Bằng cách hiểu các khái niệm cốt lõi và các thuật toán như Q-learning, DQN, và PPO, bạn đã có thể bắt đầu xây dựng các agent thông minh của riêng mình. 