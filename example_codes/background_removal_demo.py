from pathlib import Path

import cv2
import retro


ENV_NAME = 'MortalKombatII-Genesis'
STATE_NAME = 'Level1.BotVsBot'
STATE_PATH = Path(f'../states/{STATE_NAME}.state').resolve()

BACKGROUND = cv2.imread('../assets/level1_background.png')


env = retro.make(ENV_NAME,
                 use_restricted_actions=retro.Actions.ALL,
                 state=str(STATE_PATH),
                 players=2,
                 scenario="scen.json")

HEIGHT, WIDTH, *_ = env.reset().shape


def main():
    obs, *_ = env.step('0'*24)
    obs = obs[:, :, ::-1]
    env.render()

    res = cv2.matchTemplate(BACKGROUND, obs, cv2.TM_SQDIFF_NORMED)
    min_, _, min_loc, _ = cv2.minMaxLoc(res)
    if min_ < 0.3:
        x, y = min_loc[1], min_loc[0]

        diff = cv2.cvtColor(BACKGROUND[x:x+HEIGHT, y:y+WIDTH] - obs, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

        cv2.imshow('output', mask)
        cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main()

