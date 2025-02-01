// new_low_level.cpp

#include <Eigen/Dense>
#include <chrono>
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <vector>

using json = nlohmann::json;
const std::string TASK_URL = "http://127.0.0.1:8000";

// Fetch a task (as JSON) from the proxy server.
json fetchTask() {
  cpr::Response r = cpr::Get(cpr::Url{TASK_URL});
  if (r.status_code != 200) {
    throw std::runtime_error("Failed to fetch task, HTTP status: " +
                             std::to_string(r.status_code));
  }
  std::cout << "Task received successfully!" << std::endl;
  return json::parse(r.text);
}

// Send the result (as JSON) back to the proxy server.
void postResult(const json &resultJson) {
  cpr::Response r = cpr::Post(cpr::Url{TASK_URL},
                              cpr::Header{{"Content-Type", "application/json"}},
                              cpr::Body{resultJson.dump()});
  if (r.status_code == 200) {
    std::cout << "Results sent successfully!" << std::endl;
  } else {
    std::cerr << "Error sending results: HTTP " << r.status_code << std::endl;
  }
}

int main() {
  try {
    while (true) {
      // 1. Retrieve a task
      json taskJson = fetchTask();

      // 2. Extract the matrix "a" and vector "b" from the JSON
      std::vector<std::vector<double>> a_data =
          taskJson["a"].get<std::vector<std::vector<double>>>();
      std::vector<double> b_data = taskJson["b"].get<std::vector<double>>();

      size_t rows = a_data.size();
      if (rows == 0) {
        std::cerr << "Empty matrix received." << std::endl;
        continue;
      }
      size_t cols = a_data[0].size();

      // Build Eigen matrix A
      Eigen::MatrixXd A(rows, cols);
      for (size_t i = 0; i < rows; ++i) {
        if (a_data[i].size() != cols) {
          std::cerr << "Inconsistent row sizes in matrix." << std::endl;
          continue;
        }
        for (size_t j = 0; j < cols; ++j) {
          A(i, j) = a_data[i][j];
        }
      }

      // Build Eigen vector B
      Eigen::VectorXd B =
          Eigen::Map<Eigen::VectorXd>(b_data.data(), b_data.size());

      // 3. Solve the system Ax = b and measure the execution time.
      auto start = std::chrono::high_resolution_clock::now();
      Eigen::VectorXd X = A.llt().solve(B);
      auto end = std::chrono::high_resolution_clock::now();
      std::chrono::duration<double> duration = end - start;
      double exec_time = duration.count();

      // 4. Add the result vector "x" and the execution time "time" to the JSON.
      std::vector<double> x_vec(X.data(), X.data() + X.size());
      taskJson["x"] = x_vec;
      taskJson["time"] = exec_time;

      std::cout << "Task solved in " << exec_time << " seconds." << std::endl;

      // 5. Send the result back to the proxy server.
      postResult(taskJson);
    }
  } catch (const std::exception &e) {
    std::cerr << "Exception: " << e.what() << std::endl;
  }
  return 0;
}
