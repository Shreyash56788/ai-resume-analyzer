import time

from app.performance import PerformanceTimer


def test_performance_timer():

    timer = PerformanceTimer()

    time.sleep(0.1)

    first_checkpoint = timer.checkpoint(
        "stage_1"
    )

    time.sleep(0.1)

    second_checkpoint = timer.checkpoint(
        "stage_2"
    )

    total_time = timer.get_total_time()

    checkpoints = timer.get_checkpoints()

    print("\n========== PERFORMANCE TIMER TEST ==========")

    print(
        f"Stage 1: {first_checkpoint} seconds"
    )

    print(
        f"Stage 2: {second_checkpoint} seconds"
    )

    print(
        f"Total: {total_time} seconds"
    )

    print(
        f"Checkpoints: {checkpoints}"
    )

    print(
        "============================================"
    )

    assert first_checkpoint >= 0.1
    assert second_checkpoint >= first_checkpoint
    assert total_time >= second_checkpoint

    assert "stage_1" in checkpoints
    assert "stage_2" in checkpoints

    print(
        "\n🎉 Performance timer test passed!"
    )


if __name__ == "__main__":

    test_performance_timer()