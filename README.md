## Cheeky Monkey

Inspired by Netflix's "[Chaos Monkey](https://github.com/Netflix/chaosmonkey)", this game quite literally sets a monkey loose in your Kubernetes cluster.   

&nbsp;

<p align="center">
<img src="https://raw.githubusercontent.com/richstokes/cheekymonkey/master/images/screenshot.png" width="75%">
</p>

>CHAOS ENGINEERING IS:
>"the discipline of experimenting on a distributed system in order to build confidence in the system's capability to withstand turbulent conditions in production."

&nbsp;

Kubernetes pods are represented by crates in the game. The more pods you have, the more crates are dropped!  

You can control the monkey with the arrow keys, and punch crates with spacebar.  

Every time the monkey destroys a crate, a pod in your cluster is randomly selected and deleted.  

&nbsp;

### Install & run

1. Clone the repo
2. `pip3 install -r requirements.txt`
3. `python3 main_window.py`

Unless offline mode is set (see below), the game will attempt to connect to your currently set Kubernetes context.  

Note: The game will target pods across ALL namespaces.  


&nbsp;

#### Command line Options

`--offline yes`  Switches to offline mode, no pods will be harmed


&nbsp;

#### Other settings

Change the following in `constants.py`:

- Resolution - set `SCREEN_WIDTH`  and `SCREEN_HEIGHT` as desired
- `CONTAINER_FACTOR` - Multiplication factor for creating crates based on the actual number of containers in your cluster
- `CONTAINER_HEALTH` - How many times the monkey needs to hit the crate before its pod is killed
- `OFFLINE_CRATE_COUNT` - How many crates to spawn in offline mode (Multiplied by `CONTAINER_FACTOR`)


&nbsp;

## Credits

- [Monkey character sprites](https://www.gameartguppy.com/shop/monkey-game-character-sprites/ )
- [Python Arcade Library](https://arcade.academy/index.html)
