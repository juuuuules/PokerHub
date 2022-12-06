import os


def simulate(user1, user2, opp1, opp2, board, board1, board2, board3, board4, board5):
    print(user1)
    if not board:
        output_stream = os.popen(
            f"python3 ./holdem_calc-master/holdem_calc.py {user1} {user2} {opp1} {opp2}")
    else:
        output_stream = os.popen(
            f"python3 ./holdem_calc-master/holdem_calc.py {user1} {user2} {opp1} {opp2} -b {board1} {board2} {board3} {board4} {board5}")

    # Getting results from command line and cleaning into the winning percentages and histograms
    results = output_stream.read().split("\n\n")[:-1]
    results[0] = results[0].split("\n")[1:]
    results[1] = results[1].split("\n")[1:]
    results[2] = results[2].split("\n")[1:]
    results[0] = [result.split(": ")[1:][0] for result in results[0]]
    results[1] = [result.split(":") for result in results[1]]
    results[2] = [result.split(":") for result in results[2]]
    return results
