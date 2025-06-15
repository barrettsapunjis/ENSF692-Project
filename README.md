# ENSF692-Project
Data analysis group project. The purpose of the project is to combine 3 seperate (but related) data sets and create a UI for a user to query the combined dataset. 

members: Marley Cheema, Barrett Sapunjis 

<<<<<<< HEAD
Expected dataset: 

| Movie ID | Movie Name | Movie details.... | Actors | Actor details |
| -------- | ---------- | ----------------- | ------ | ------------- |
| 1        | inglorious bastards     |10/10                    | {actor 1, actor 2}      |  { 1984 , 1990}           |

there is a possiblity that the actors can be made into a hierarchial key and do not need to be in a list. 
=======
Expected hierarchy: 

- **Team** (all NHL teams - 32 rows)
	- **Situation** (5v5, 4v5, 5v4, other, all - 5 rows per team)
		- **Stats** (# of players + 1 rows)
			- Contains player stats per situation
			- contains goalie stats per situation
			- contains total team stats per situation 

>>>>>>> b789dc6884fe71b0830105fbcafca9957ea5ebc2


- how to use:
   	- `pip install -r requirements.txt`
   	- `python .\main.py`



```mermaid graph TD
classDiagram
	class Flask {
	    + Flask(__name__)
	}
	
	class App {
	    - df: DataFrame
	    + index() str
	}
	
	class Main {
	    + main() void
	}
	
	class IndexTemplate {
	    + render(keyword1: str, keyword2: str, table: str) html
	}
	
	Flask <|-- App
	Main --> App
	App --> IndexTemplate

```