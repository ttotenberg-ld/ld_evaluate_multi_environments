# What is this?
It's a way to evaluate flags across multiple LaunchDarkly environments. Used to populate demo instances. It will evaluate all flags in the environments of your choice every 30 seconds.

Go from this:
![before](media/before.png)

To this:
![after](media/after.png)

# How can I use it?
1. `pip install requirements.txt`
2. Rename `.env.example` to `.env`
3. Replace the environment variables in `.env` with your values.
4. `python main.py`
5. Press `ctrl/cmd + c` to stop the process