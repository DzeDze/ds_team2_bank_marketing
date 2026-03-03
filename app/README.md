# HOW TO CREATE YOUR STREAMLIT PAGE

### Run the Streamlit app locally

Run these command at the root folder of the project:

`git pull origin main`

`uv sync`

`uv pip install -e .`

`uv run streamlit run app/main.py `

### Create your own reports

We will decide later which charts to display, all in a single page or we need multi-pages, and will follow Kateryna wire-frame. But you can try to play around first with your charts.

1. Put your file under `app/pages/your-file.py`
2. The current set app will automatically recognize your page (`your-file.py`) and add it into the sidebar. Your file name will become how it shown n the sidebar.
3. If you have doubt, read one of the example I have already put into `app/pages/xx_YourName_Example.py`. All the code there I just copied form your notebook, so you should very familiar with it. I added an example of how to display plotly too, based on your matplotlib/ seaborn charts, so you could also see if you can produce some plotly plots if needed for more interactive plots.

Feel free to ask me on `Slack` if you have any questions.
