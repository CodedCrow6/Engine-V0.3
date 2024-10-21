This is a custom-built fighting game engine designed to bring much needed features to the pygame-ce framework ,The goal is to end up with a modern game engine capable of bringing to life a Commercial quality game with all the modern trappings as well as improved  flexibility and ease of use removing limitation and unneccessary frustration for the developers and designers that this tool is intended for .Its current state the engine is far from this thought so inorder to improve the expression of my vision for this project some of the current implemented features are listed below ,futher more below that there is a rather extensive list of planned feature implementation


IMPLEMENTED FEATURES

  Customizable Characters - Using a Modular approach to handling character attributes, states, and attacks. This "bolt-on" approach to character creation allows for the simplified addtion/removal of character related mechanics.
                              Simply add to the list of imports items such as healthbars , special meters and custom object animators. Create a balanced and unique gaming experience by introducing character specific attributes , ablities and buffs .This can be achieved                                 by adding the fields into the characters data file, which can be formatted using json like syntax.

  Automated Sprite Extraction system - A fully functional automated spritesheet classification and sprite animation extraction tool, which serves to take the hasstle out of manually processing the locations of every frame on a spritesheet.Relying on colorkeys the tool                                                                         iterates through each pixel to determine the bounding rectuangle of the sprite , this ensures that if properly configured ,the result is a seamless animation.

  Modular and customizable Game State Machine - To be continued !!!!!!!!!!!!!!!!!!
