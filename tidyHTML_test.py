"""Theresa Breiner and Ryan Smith, HW 4, CIT 591"""
import unittest
from tidyHTML import *
class newtidy(unittest.TestCase):

	def test_find_tag(self):
		self.assertEqual(['<tag>', 4, 9], find_tag('west<tag> this sentence continues'))
		self.assertEqual(['<zebra wertyu>', 3, 17], find_tag('www<zebra wertyu>'))
		self.assertEqual(-1, find_tag('sfdfsdfs'))

	def test_find_tag_name(self):
		self.assertEqual('fred', find_tag_name('<fred eeffsdfgdsg.www.com>'))
		self.assertEqual('georgia', find_tag_name(' <GEORGIA/>'))
		self.assertEqual('georgia', find_tag_name(' < GEORGIA/>'))
		self.assertEqual('georgia', find_tag_name(' < GEORGIA />'))
		self.assertEqual('georgia', find_tag_name(' < GEORGIA / >'))

	def test_get_tag(self):
		self.assertEqual(['zebra', 3, 17], get_tag('www<zebra wertyu>'))
		self.assertEqual(-1, get_tag('dondfonsdfon'))

	def test_is_first_on_line(self):
		self.assertTrue(is_first_on_line('<panther>fdsfdsfsdf', 'panther'))
		self.assertFalse(is_first_on_line('dfdfsdf<jaguar>', 'jaguar'))

	def test_is_first_tag_in_line(self):
		self.assertTrue(is_first_tag_in_line('<first>some text', 0))
		self.assertTrue(is_first_tag_in_line('some text <first> more', 10))
		self.assertFalse(is_first_tag_in_line('<first> text <second>', 13))
		self.assertTrue(is_first_tag_in_line('text \nmore <first> yay', 11))
		self.assertFalse(is_first_tag_in_line('text \n some <tag> and <ours>', 22))

	def test_is_pre_tag(self):
		self.assertTrue(is_pre_tag('pre'))
		self.assertFalse(is_pre_tag('cobra'))

	def test_is_empty_tag(self):
		self.assertTrue(is_empty_tag('area'))
		self.assertFalse(is_empty_tag('gazelle'))
		self.assertTrue(is_empty_tag('br'))

	def test_is_end_tag(self):
		self.assertTrue(is_end_tag('/florida'))
		self.assertFalse(is_end_tag('florida'))

	def test_is_start_tag(self):
		self.assertTrue(is_start_tag('p'))
		self.assertFalse(is_start_tag('/head'))
		self.assertFalse(is_start_tag('area'))
		self.assertFalse(is_start_tag('pre'))

	def test_is_header_tag(self):
		self.assertTrue(is_header_tag('head'))
		self.assertFalse(is_header_tag('/head'))
		self.assertFalse(is_header_tag('openbrackets'))

	def test_is_there_an_end_tag(self):
		self.assertTrue(is_there_end_tag('<tag>giraffes are tall </tag>', 'tag'))
		self.assertFalse(is_there_end_tag('<tag>giraffes are tall </tag>', 'tags'))
	
	def test_is_in_tag_list(self):
		set_tag_list(['a', 'b', 'c'])
		self.assertTrue(is_in_tag_list('a'))
		self.assertFalse(is_in_tag_list('d'))

	def test_fix_nesting(self):
		set_tag_list(['a', 'b'])
		self.assertEqual(['<a><b>\n  </b>\n</a>\n', 19], fix_nesting('<a><b></a>', '/a', 6, 10))
		self.assertEqual([], get_tag_list())

		set_tag_list(['a', 'b'])
		self.assertEqual(['<a><b>', 6], fix_nesting('<a><b></c>', '/c', 6, 10))
		self.assertEqual(['a', 'b'], get_tag_list())

	def test_delete_tag(self):
		self.assertEqual('<a><b></b>', delete_tag('<a><b></a></b>', '/a', 6, 10))
		self.assertEqual('<a><b>', delete_tag('<a><b></c>', '/c', 6, 10))

	def test_create_and_insert_tag(self):
		set_tag_list(['a', 'b', 'c'])
		self.assertEqual(['<a><b><c>\n    </c>\n  </b>\n</a>', 30], create_and_insert_tag('<a><b><c></a>', 0, 9, 13))
		self.assertEqual([], get_tag_list())

		set_tag_list(['a', 'b', 'c'])
		self.assertEqual(['<a><b><c>\n    </c>\n  </b><a>', 25], create_and_insert_tag('<a><b><c></b><a>', 1, 9, 13))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a', 'b', 'c'])
		self.assertEqual(['<a><b><c>text sample\n    </c>\n  </b></a>', 36], create_and_insert_tag('<a><b><c>text sample</b></a>', 1, 20, 24))
		self.assertEqual(['a'], get_tag_list())

	def test_find_tag_list_index(self):
		set_tag_list(['a', 'b', 'c'])
		self.assertEqual(0, find_tag_list_index('a'))
		self.assertEqual(2, find_tag_list_index('c'))

	def test_is_in_tag_list(self):
		set_tag_list(['a', 'b', 'c'])
		self.assertTrue(is_in_tag_list('a'))
		self.assertTrue(is_in_tag_list('c'))
		self.assertFalse(is_in_tag_list('d'))
		self.assertFalse(is_in_tag_list('crazytime'))

	def test_both_tags_in_line(self):
		set_tag_list([])
		local_tag_list = []
		self.assertEqual(25, both_tags_in_line('<a><b><c><br></c></b></a>', 'a', 3))
		self.assertEqual([], get_tag_list())

		set_tag_list([])
		local_tag_list = []
		self.assertEqual(-1, both_tags_in_line('<a><b></b>', 'a', 3))
		self.assertEqual(['a'], get_tag_list())

	def test_indent(self):
		set_tag_list(['a'])
		self.assertEqual('  <header> with text', indent('<header> with text', 0))
		self.assertEqual('some text   <header> more', indent('some text <header> more', 10))

		set_tag_list(['a', 'b'])
		self.assertEqual('    <code> text </code>', indent('<code> text </code>', 0))

		set_tag_list([])
		self.assertEqual('<example>', indent('<example>', 0))

	def test_find_pre_end_tag(self):
		self.assertEqual(27, find_pre_end_tag('<pre>texttexttexttext</pre>text'))
		self.assertEqual(-1, find_pre_end_tag('<pre>texttexttexttext<pre>text'))

	def test_insert_new_line(self):
		self.assertEqual('\nneeds new line', insert_new_line('needs new line', 0))
		self.assertEqual('not yet but \nnow', insert_new_line('not yet but now', 12))

	def test_handle_pre_tag(self):
		set_tag_list(['sdsd'])
		set_need_end_pre(False)
		self.assertEqual(['text\n  <pre>text</pre>', 22], handle_pre_tag('text<pre>text</pre>', 'pre', 4))
		self.assertFalse(get_need_end_pre())

		set_need_end_pre(False)
		self.assertEqual(['  <pre>texttext</pre>text', 21], handle_pre_tag('<pre>texttext</pre>text', 'pre', 0))
		self.assertFalse(get_need_end_pre())

		set_need_end_pre(False)
		self.assertEqual(['  <pre>texttext  ', -1], handle_pre_tag('<pre>texttext  ', 'pre', 0))
		self.assertTrue(get_need_end_pre())

		set_need_end_pre(False)
		self.assertEqual(['  <pre> text </pre>', 19], handle_pre_tag('<pre> text </pre>', 'pre', 0))
		self.assertFalse(get_need_end_pre())

	def test_handle_missing_end_pre(self):
		set_tag_list(['a'])
		set_need_end_pre(True)
		self.assertEqual(['texttexttext', -1], handle_missing_end_pre('texttexttext'))
		self.assertTrue(get_need_end_pre())

		set_need_end_pre(True)
		self.assertEqual(['text</pre>text', 10], handle_missing_end_pre('text</pre>text'))
		self.assertFalse(get_need_end_pre())

		set_need_end_pre(True)
		self.assertEqual(['text</pre>', 10], handle_missing_end_pre('text</pre>'))
		self.assertFalse(get_need_end_pre())

	def test_handle_empty_tag(self):
		set_tag_list(['a'])
		self.assertEqual(['  sometext<br>text', 14], handle_empty_tag('sometext<br>text', 8, 12))

		set_tag_list(['a'])
		self.assertEqual(['  <br>stuff', 6], handle_empty_tag('<br>stuff', 0, 4))

	def test_handle_initial_indent(self):
		set_tag_list(['a'])
		self.assertEqual(['  something</tag>', 2], handle_initial_indent('something</tag>', 9))


	def test_handle_start_tag(self):
		set_tag_list(['a'])
		self.assertEqual(['  <tag>test</tag>', 17], handle_start_tag('<tag>test</tag>', 'tag', 0, 5))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual(['  text<tag>test</tag>', 21], handle_start_tag('text<tag>test</tag>', 'tag', 4, 9))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual(['\n  <tag>some text <another>', 8], handle_start_tag('<tag>some text <another>', 'tag', 0, 5))
		self.assertEqual(['a', 'tag'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual(['  text\n  <tag> more text <more>', 14], handle_start_tag('text<tag> more text <more>', 'tag', 4, 9))
		self.assertEqual(['a', 'tag'], get_tag_list())

	def test_handle_end_tag(self):

		set_tag_list(['first', 'code', 'second', 'third'])
		self.assertEqual(['        text text \n      </third>\n tr', 34], handle_end_tag('text text </third> tr', '/third', 10, 18))

		set_tag_list(['first', 'code', 'second', 'third'])
		self.assertEqual(['        end of sentence.\n      </third>\n    </second>\n  </code>\n <open> Beginning', 64], handle_end_tag('end of sentence.</code> <open> Beginning', '/code', 16, 23))
		self.assertEqual(['first'], get_tag_list())

		set_tag_list(['first', 'second', 'third'])
		self.assertEqual(['      end of sentence. <open> Beginning', 22], handle_end_tag('end of sentence.</code> <open> Beginning', '/code', 16, 23))
		self.assertEqual(['first', 'second', 'third'], get_tag_list())

		set_tag_list(['first', 'second', 'third'])
		self.assertEqual(['end of<tag> sentence. <open> Beginning', 21], handle_end_tag('end of<tag> sentence.</code> <open> Beginning', '/code', 21, 28))
		self.assertEqual(['first', 'second', 'third'], get_tag_list())



	def test_handle_header(self):
		set_tag_list(['a'])
		self.assertEqual(['\n  <header>', 11], handle_header('<header>', 'header', 0, 8))
		self.assertEqual(['a', 'header'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual(['  text\n\n  <header>', 18], handle_header('text<header>', 'header', 4, 12))
		self.assertEqual(['a', 'header'], get_tag_list())

		set_tag_list(['a', 'open'])
		self.assertEqual(['<open>\n\n    <header>great', 20], handle_header('<open><header>great', 'header', 6, 14))
		self.assertEqual(['a', 'open', 'header'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual(['\n  <header> some </header>', 26], handle_header('<header> some </header>', 'header', 0, 8))
		self.assertEqual(['a'], get_tag_list())

	def test_process_line(self):

		set_tag_list(['a'])
		self.assertEqual('  <pre> text </pre>', process_line('<pre> text </pre>'))

		set_tag_list(['a'])
		self.assertEqual('  <pre> <ignore></pre>', process_line('<pre> <ignore></pre>'))

		set_tag_list(['a'])
		set_need_end_pre(True)
		self.assertEqual('<ignore>text </end>', process_line('<ignore>text </end>'))
		self.assertEqual(['a'], get_tag_list())
		self.assertTrue(get_need_end_pre())

		set_tag_list(['a'])
		set_need_end_pre(True)
		self.assertEqual('<ignore>text </end></pre>', process_line('<ignore>text </end></pre>'))
		self.assertEqual(['a'], get_tag_list())	
		self.assertFalse(get_need_end_pre())

		set_tag_list(['a'])
		set_need_end_pre(False)
		self.assertEqual('\n  <head>', process_line('<head>'))
		self.assertEqual(['a', 'head'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual('  text\n\n  <head>', process_line('text<head>'))
		self.assertEqual(['a', 'head'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual('\n  <open>\n\n    <head>great', process_line('<open><head>great'))
		self.assertEqual(['a', 'open', 'head'], get_tag_list())

		set_tag_list(['a'])
		self.assertEqual('\n  <head> some </head>', process_line('<head> some </head>'))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a', 'b'])
		self.assertEqual('    text\n  </b>', process_line('text</b>'))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a', 'b'])
		self.assertEqual('    text', process_line('text</c>'))
		self.assertEqual(['a', 'b'], get_tag_list())

		set_tag_list(['a', 'b', 'c'])
		self.assertEqual('      text\n    </c>\n  </b>\n', process_line('text</b>'))
		self.assertEqual(['a'], get_tag_list())

		set_tag_list(['a', 'b'])
		self.assertEqual('    <friend><cat></cat></friend>', process_line('<friend><cat></cat></friend>'))
		self.assertEqual(['a', 'b'], get_tag_list())				

		set_tag_list(['a', 'b'])
		self.assertEqual('    text\n    <friend><cat></cat>', process_line('text<friend><cat></cat>'))
		self.assertEqual(['a', 'b', 'friend'], get_tag_list())	

		set_tag_list(['a'])
		self.assertEqual('  text\n  <tag> more text \n    <more>', process_line('text<tag> more text <more>'))
		self.assertEqual(['a', 'tag', 'more'], get_tag_list())	

		set_tag_list(['a'])
		self.assertEqual('  text<a><b><br></b></a>', process_line('text<a><b><br></b></a>'))
		self.assertEqual(['a'], get_tag_list())
	

	def test_make_whitespace(self):
		self.assertEqual('    ', make_whitespace(4))

	def test_cut_line(self):
		self.assertEqual("  jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd\n  jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd ", cut_line('  jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd ', '  '))
		self.assertEqual("  jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd\n  jhkkvkvkkhsbld ks lk skdjl sdsds", cut_line('  jhkkvkvkkhsbld ks lk skdjl sdsds kksbls dk k khs kdsvkdskd ksj d dkj skd ksd jhkkvkvkkhsbld ks lk skdjl sdsds', '  '))

unittest.main()
