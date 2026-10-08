import subprocess,sys,unittest
import minesmurre as m
class MineTests(unittest.TestCase):
    def test_lazy_placement(self):self.assertIsNone(m.Game().mines)
    def test_first_safe_many(self):
        for seed in range(50):
            g=m.Game(seed=seed);g.reveal(4,4);self.assertFalse(g.lost);self.assertTrue((set(g.neighbors((4,4)))|{(4,4)}).isdisjoint(g.mines));self.assertEqual(len(g.mines),10)
    def test_corners_safe(self):g=m.Game(seed=4);g.reveal(0,0);self.assertEqual(g.number((0,0)),0)
    def test_deterministic(self):a=m.Game(seed=1);b=m.Game(seed=1);a.reveal(0,0);b.reveal(0,0);self.assertEqual(a.mines,b.mines)
    def test_invalid_settings(self):
        for size,count in ((3,1),(13,1),(4,0),(4,8),(True,1)):
            with self.assertRaises(ValueError):m.Game(size,count)
    def test_bounds(self):
        g=m.Game()
        with self.assertRaises(ValueError):g.reveal(-1,0)
        with self.assertRaises(ValueError):g.flag(0,8)
    def test_flag_toggle(self):g=m.Game();g.flag(1,1);self.assertIn((1,1),g.flags);g.flag(1,1);self.assertNotIn((1,1),g.flags)
    def test_flag_blocks_reveal(self):
        g=m.Game();g.flag(0,0)
        with self.assertRaises(ValueError):g.reveal(0,0)
        self.assertIsNone(g.mines)
    def test_flag_limit(self):
        g=m.Game(4,1);g.flag(0,0)
        with self.assertRaises(ValueError):g.flag(0,1)
    def test_open_cannot_flag(self):
        g=m.Game(seed=1);g.reveal(0,0)
        with self.assertRaises(ValueError):g.flag(0,0)
    def test_repeat_reveal_no_action(self):g=m.Game(seed=1);g.reveal(0,0);n=g.actions;self.assertFalse(g.reveal(0,0));self.assertEqual(g.actions,n)
    def test_hit_mine(self):g=m.Game(seed=1);g.reveal(0,0);pos=next(iter(g.mines));g.reveal(*pos);self.assertTrue(g.lost);self.assertFalse(g.won())
    def test_win_by_safe_cells(self):
        g=m.Game(seed=3);g.reveal(0,0)
        for r in range(g.size):
            for c in range(g.size):
                if (r,c) not in g.mines and not g.won():g.reveal(r,c)
        self.assertTrue(g.won());self.assertFalse(g.lost)
    def test_numbers(self):g=m.Game(4,1);g.mines={(1,1)};self.assertEqual(g.number((0,0)),1);self.assertEqual(g.number((3,3)),0)
    def test_cli(self):r=subprocess.run([sys.executable,'minesmurre.py','--seed','1'],input='r 1 1\nq\n',capture_output=True,text=True);self.assertEqual(r.returncode,0);self.assertIn('MINESMURRE',r.stdout)
    def test_demo(self):r=subprocess.run([sys.executable,'minesmurre.py','--demo','--seed','1'],capture_output=True,text=True);self.assertEqual(r.returncode,0);self.assertIn('Revealed:',r.stdout)
if __name__=='__main__':unittest.main()

class FallbackTests(unittest.TestCase):
 def test_no_curses_demo(self):
  import minesmurre,io
  from unittest.mock import patch
  from contextlib import redirect_stdout
  with patch.object(minesmurre,'curses',None),redirect_stdout(io.StringIO()) as out:
   self.assertEqual(minesmurre.main(['--demo','--seed','42']),0)
  self.assertIn('MINESMURRE',out.getvalue())
