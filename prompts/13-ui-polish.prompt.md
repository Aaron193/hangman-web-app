the figure works now, thanks. a few ui things I noticed while testing:

1. on a phone (375px wide) the word pattern sits next to the drawing and long words wrap in the middle of the word (a 9 letter word breaks onto two lines). at narrow widths put the pattern on its own full-width row under the drawing, and size the font so a 12 letter word fits on one line at 375px.
2. the won/lost message is just small bold text and it's easy to miss. make it stand out: a banner with bigger text, green for a win and red for a loss. keep the words "You won!" / "You lost." so it doesn't rely on colour alone, and keep error messages looking like errors.
3. when a game ends, move keyboard focus to the New game button so you can just hit enter to go again.

keep the figure working (check the computed display again), keep the tests passing, no commits.
