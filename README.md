## Cheeky Monkey

Inspired by Netflix's "[Chaos Monkey](https://github.com/Netflix/chaosmonkey)", this game quite literally sets a monkey loose in your Kubernetes cluster.   

&nbsp;

<p align="center">
<img src="https://raw.githubusercontent.com/richstokes/cheekymonkey/master/images/intro.gif" width="65%">
</p>
&nbsp;

>CHAOS ENGINEERING IS:
>"the discipline of experimenting on a distributed system in order to build confidence in the system's capability to withstand turbulent conditions in production."  

This game is more for fun and demonstration purposes than to be a genuine chaos engineering tool. That said, over time I may add other disruptive features beyond simply killing pods. Feel free to open an "issue" with any suggestions!

&nbsp;

Kubernetes pods are represented by crates in the game. The more pods you have, the more crates are dropped!  

You control the monkey with the arrow keys, and punch crates with spacebar. You can also hold 'G' to grab a crate to your right and drag it around.  

Every time the monkey destroys a crate, a pod in your cluster is randomly selected and deleted.  

Press 'R' to reset the game.  


&nbsp;

### Install & run

1. Clone the repo
2. `pip install -r requirements.txt`
3. `python cheekymonkey.py`  

Or with `pyenv` (recommended):  

```
pyenv install 3.8.7
eval "$(pyenv init -)"
pyenv local 3.8.7
pip install -r requirements.txt
python ./cheekymonkey.py
```

&nbsp;

Unless offline mode is set (see below), the game will attempt to connect to your currentt Kubernetes context.  

Note: The game will target pods across ALL namespaces, unless you specify namespaces to exclude, for example:  
`python cheekymonkey.py --exclude kube-system cert-manager`


&nbsp;

#### Command line Options

`--offline yes`  Switches to offline mode, no pods will be harmed  
`--exclude <namespace1> <namespace2>`  Space-separated list of namespaces to exclude  


&nbsp;

#### Other settings

Change the following in `constants.py`:

- Resolution - set `SCREEN_WIDTH`  and `SCREEN_HEIGHT` as desired
- `CONTAINER_FACTOR` - Multiplication factor for creating crates based on the actual number of containers in your cluster. The idea is you can use this to get a reasonable number of crates in game if you have a lot of running pods in your cluster.
- `CONTAINER_HEALTH` - How many times the monkey needs to hit the crate before its corresponding pod is killed
- `OFFLINE_CRATE_COUNT` - How many crates to spawn in offline mode (Multiplied by `CONTAINER_FACTOR`)  

You can have fun with the physics by using the plus/minus keys to change the punching force.  


&nbsp;

## Credits

- [Python Arcade Library](https://arcade.academy/index.html)
- [Monkey character sprites](https://www.gameartguppy.com/shop/monkey-game-character-sprites/ )
- [CREDITS.md](https://github.com/richstokes/cheekymonkey/blob/master/CREDITS.md)

