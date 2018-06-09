**Python application for creating chess combinations.** 

Description for the task
https://drive.google.com/file/d/10i2IY1QzCT5iCGIHG6fgOg1i53a5vv0b/view?usp=sharing



_How to install_
```bash
git clone git@github.com:DmitryBurnaev/chess-challenge.git <path_to_project>
cd <path_to_project>
```

_How to test_
```bash
cd <path_to_project>
python3 -m unittest discover -v
```

_How to get a help_
```bash
cd <path_to_project>
python3 -m src.run --help

```

_How to run_
```bash
cd <path_to_project>
python3 -m src.run 3 3 --kings 1 --rooks 2

```

Below is an example of creating a combination for 1 king and 2 rooks on a 3 x 3 board.  
All results will be written to the file <path_to_project>/results.log

```bash
$ python3 -m src.run 3 3 --kings 1 --rooks 2 --file


---------Initial configuration----------
Boards dimensions: 3 x 3
Figures set:
   Kings    :  1
   Rooks    :  2
-----------------Result-----------------
Found 4 combinations:
[R] Rook (1;2) | [R] Rook (2;3) | [K] King (3;1)
    1 2 3
1 | - - K
2 | R - -
3 | - R -
--------------------
[R] Rook (2;3) | [R] Rook (3;2) | [K] King (1;1)
    1 2 3
1 | K - -
2 | - - R
3 | - R -
--------------------
[R] Rook (2;1) | [R] Rook (3;2) | [K] King (1;3)
    1 2 3
1 | - R -
2 | - - R
3 | K - -
--------------------
[R] Rook (1;2) | [R] Rook (2;1) | [K] King (3;3)
    1 2 3
1 | - R -
2 | R - -
3 | - - K
----------------------------------------

```

