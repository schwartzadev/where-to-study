# Where to Study

## Development

Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

## Deployment

Where to Study is deployed on Heroku and is served at [www.curooms.live](http://www.curooms.live)

## About

### Inspiration ✨

CU provides access to many different study spaces on campus, but they are hard to discover and it is difficult to assess their covid-19 safety.

### What it does

[Where to study](http://www.curooms.live/) combines density data from [Buff Pass](https://pass.colorado.edu/login), [CU's digital map system](https://www.colorado.edu/map/), and availability data from [CU's room reservation system](https://ems.colorado.edu/) to provide suggestions for places to study.

### How we built it 🔨
We used Django (python) for the web interface and python to scrape and cache all of the relevant data. We also used Tailwind CSS for the web interface styles.

### Challenges we ran into
Because we integrated data from a number of different sources, we encountered variability between those sources. Some rooms that students can book are not "study" rooms, for example. Building names in were formatted in different ways in different places.