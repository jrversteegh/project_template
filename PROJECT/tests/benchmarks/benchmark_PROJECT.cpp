#include <cassert>
#include <iostream>
#include <random>

#include <benchmark/benchmark.h>

#include "PROJECT/config.h"

auto rand() {
  static std::random_device rd;
  static std::mt19937 gen(rd());
  std::uniform_real_distribution<Number> dis(0.0, 1.0);
  return dis(gen);
}

static void benchmark_PROJECT(benchmark::State& state) {
  for (auto _ : state) {
    auto value = rand();
    benchmark::DoNotOptimize(value);
  }
}
BENCHMARK(benchmark_PROJECT);

BENCHMARK_MAIN();
