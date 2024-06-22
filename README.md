# Codenames AI

## Problem Overview

Codenames is a team-based card game about correctly identifying conceptually related words. In the game, two spymasters attempt to give single-word clues that identify one or more words present on the board. The other players (called field operatives) try to guess their spymaster’s words while avoiding the opposing team’s words. The first team to correctly guess all of their words wins. Furthermore, the board contains a single word called an assassin, which cannot be guessed by either team or they lose the game.

There are two ways AI can be inserted into Codenames:
1.  As a spymaster. This has a few nice things about it. Firstly, the spymaster in Codenames is supposed to be emotionless in order to not give any additional information away using body language. AI fits this role perfectly. Secondly, unlike the field operatives, the spymaster does not need to communicate with other players, simplifying the problem a bit. Finally, both of the spymasters can be replaced with AI, allowing players to play the game with fewer people while still having fun.
2. As a field operative. This is slightly harder, as there is a need to communicate with other players. However, this problem can be solved by simply giving a suggestion to the other players and letting them have the final choice of words to pick. Furthermore, unlike the spymaster, there is no need to take the team’s skill level into account for this role.

The environment can be specified using PEAS:
- Performance measure: number of words guessed correctly by the team, rate of incorrect guesses, overall win rate
- Environment: 25 words on the board, which words are marked as red agents/blue agents/innocent bystanders/assassin, team assignments, spymaster assignments
- Actuators:
  - Spymaster: single-word clue, number of words identified by the clue
  - Field operative: order of words from most likely to least likely to be the correct agent
- Sensors: command line arguments

The environment type can be described as the following:
- Fully observable as the spymaster, but only partially observable as a field operative.
- Deterministic.
- Sequential.
- Static.
- Discrete because there are only finitely many valid English words.
- Multi-agent.

## Why This Problem?

Codenames is a board game increasing in popularity. Unlike a lot of board games, Codenames relies heavily on team collaboration in order to win. By creating a bot for this game that can act as either the spymaster or the field operatives (not simultaneously), we are posed with a new problem of figuring out a way for our bot to best collaborate with their teammate. Similar to other games, by creating a bot for this game, people will be able to play against a more challenging opponent and be able to develop their skills in the game. Additionally, by incorporating general knowledge levels of the bot's teammate, a Codenames AI bot would help increase the outreach of the game.

Currently, there are not too many Codename AIs that exist. Out of the ones that do exist, however, they seem to be using Word2Vec, GloVe, and WordNet to train their AI model to understand the relationships between the different words. They do this by creating a vocabulary off of Wikipedia articles as they are typically the most common words. However, when the AI is the spy master, it appears as though the majority of the AIs that do exist seem to be maximizing the number of words guessed in each move rather than minimizing the total number of moves required. While there are certainly similarities between the two, using a greedy algorithm to maximize the number of words guessed may not be the most optimal in this situation as you could have a large set of very similar words, and then a set of very dissimilar words. As such, since our AI is being created to play alongside a human, we would opt to minimize the number of clues given. By grouping words in different combinations, we would be able to find out the most efficient group and thus, minimize the number of moves. From there, we can incorporate similar ideas as those we have seen elsewhere and return the grouping with the highest score first. This ensures a more probable victory as we are considering all the possible groupings for not only this round but for future rounds as well.

Similar to playing the role of spymaster, an alternate role that our AI bot could assume is that of a field operative/guesser. The existing Codename AIs for this are the same ones as mentioned in the part above. Similarly a lot of these AI’s use a knowledge base of 30,000-40,000 most common words from wikipedia articles and create multiple-word vector mappings for each of them. For being a field operative, we are provided all the words representing the game board and the clue, either human/AI generated. These AIs build on the assumption that the given “clue” belongs from the existing thousands of common words in the knowledge base. Thus, the AI in the role of the guesser, attempts matching the word vector mappings that belong to the clue with the available words on the game board for its decision making while trying to match exactly at least n (number provided with the clue) words. In the case of a mixed AI/Human team, with a human Spymaster and an AI field agent, models added a confusion matrix in the algorithm to account for the noise and difference in the knowledge base of the AI and user. Our model for AI guessers would be similar to a model that focuses on winning the game with the least amount of hints, thus trying to maximize the number of guessed words with every given clue. In existing AIs when tested in an AI/AI environment are near 100% accurate since the knowledge base for both are exactly the same thus the matchings between words are driven from the same wikipedia word associations while the combination of Human/AI team took more turns to finish the game with word selection accuracy slightly dropping, which is expected behavior since the knowledge bases for human and AI model are different.

## Resources

Regardless of whether the AI is playing as a spymaster or a field operative, it will need to have the ability to tell how related any two words are to each other. Furthermore, the spymaster can only use valid English words as clues. Therefore, two resources are needed for this project:
A list of English words.
A database of English text or an alternative way to find relationships between words.

Luckily, both of the resources above should be readily available on the Internet.

## Risk Management

One issue that can greatly slow down our progress on the project is the enormous size and complexity of the “action space” for the AI, which in this case is all words in the English language. In addition to their dictionary definitions, certain English words also have alternative, “slang” definitions, and how such words get interpreted is highly dependent on the age group and culture of the human that the AI is playing alongside. These nuances can result in the human and/or the AI misinterpreting the provided clue. If we are struggling to get past this issue, we can make the assumption that the humans playing the game are in the same age group (e.g. in their 20s) and are from the same country (e.g. America). This assumption will also provide us with some direction in terms of finding text datasets for our AI model to learn from.

Another issue that we could face is running out of time to code both the spymaster and the field operative, given that they both will require different approaches. To address this, we could limit the scope of our project to just one of these roles. Specifically, we can focus on implementing the spymaster rather than the field operative because the spymaster seems to be more AI-friendly in terms of the problem statement.
