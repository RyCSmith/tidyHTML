"""Theresa Breiner and Ryan Smith, HW 4, CIT 591"""
"""Makes a nice, tidy file from a given HTML document."""
import shutil
import random
import os
import sys
import Tkinter
import tkFileDialog
import textwrap

tag_list = [ ]
need_end_pre = False

"""Administrative functions"""

def make_backup(file_name):
	"""Makes a backup of the given file_name by adding .bak."""

	new_name = file_name + '.bak'
	shutil.copyfile(file_name, new_name)

def make_output_file_name():
	"""Generates a random file_name and creates a new output file. Returns the file name."""

	rand_name = str(random.randint(1, sys.maxint)) + '.html'
	return rand_name

def get_file_path():
	"""Opens a user interface window to choose a file path and returns the path."""

	Tkinter.Tk().withdraw()
	in_path = tkFileDialog.askopenfilename()
	return in_path

def count_file_lines():
	"""Counts number of lines in html file."""
	counter = 0 
	file_path = get_file_path()
	file = open(file_path, 'r')
	keep_going = True
	while keep_going:
		line = file.readline()
		if not line: break
		counter = counter + 1
		ready = True
	file.close()
	return [counter, file_path]


"""Part 2 - Cutting Lines Functions"""

def cut_line(line, indent_spaces):
	"""Takes a line of over 80 characters, cuts it and adds newline plus indent
	at first white space before 80 characters. Repeats. Returns line."""
	if len(line) < 79:
		return line
	starting_spot = 79
	while line[starting_spot] != ' ':
		starting_spot -= 1
	line = line[0 : starting_spot] + '\n' + indent_spaces + cut_line(line[starting_spot + 1:], indent_spaces)
	return line



def make_whitespace(whitespaces):
	indent_builder = ''
	for number in range(whitespaces):
		indent_builder += ' '
	return indent_builder

"""Helper functions"""

def find_tag(line):
	"""Takes a line, finds what is between the signs, returns both tag_string, start_ind, and end_ind"""
	
	tag_index = line.find('<')
	if tag_index != -1:
		if line[tag_index + 1].isalpha() or line[tag_index + 1] == '/' or line[tag_index + 1] == '!':
			if line[tag_index:].find('>') == -1:
				index_after_tag = line[tag_index:].find(' ') + tag_index + 1
			else:
				index_after_tag = line[tag_index:].find('>') + tag_index + 1
		full_tag = line[tag_index:index_after_tag]
		return [full_tag, tag_index, index_after_tag]
	return -1

def find_tag_name(full_tag_string):
	"""Takes string, returns just the tag name with no excess spaces or words
	Keeps first / in end 
	Makes it all lowercase"""
	
	full_tag_string = full_tag_string.lstrip()
	full_tag_string = full_tag_string[1:].lstrip()
	first_space = full_tag_string.find(' ')
	first_bracket = full_tag_string.find('>')
	if first_space > 0:
		index_after_tag_name = first_space
	elif first_bracket > 0:
		index_after_tag_name = first_bracket
	tag = full_tag_string[0:index_after_tag_name]
	tag = tag.rstrip('/')
	tag = tag.rstrip(' ')
	tag = tag.lower()
	return tag

def get_tag(line):
	"""Takes line, finds first tag in line, returns tag_name, start_ind, end_ind"""
	
	tag_info = find_tag(line)
	if tag_info != -1:
		tag = find_tag_name(tag_info[0])
		tag_index = tag_info[1]
		index_after_tag = tag_info[2]
		return [tag, tag_index, index_after_tag]
	return -1

def is_first_on_line(line, tag):
	"""Takes line and tag, returns True if there are no characters before the tag, 
	returns False otherwise."""
	
	tag = '<' + tag
	index_of_tag = line.find(tag)
	if index_of_tag == 0:
		return True
	return False

def is_first_tag_in_line(line, start_ind):
	"""Takes line and start_ind, searches back from start_ind to find closest newline or index 0,
	from newline index, calls find_tag between newline and start_ind.
	If there is no tag between newline and start_ind, returns True, else False."""

	newline_location = line[0:start_ind].rfind('\n')
	if newline_location == -1:
		if find_tag(line[:start_ind]) == -1:
			return True
		else:
			return False
	if find_tag(line[newline_location:start_ind]) == -1:
		return True
	else:
		return False


def is_pre_tag(tag):
	"""Takes tag, checks if it is pre, returns True or False"""
	
	if tag == 'pre':
		return True
	return False

def is_empty_tag(tag):
	"""Takes tag, compares to given list of empty content tags, returns True if it's in list, else False."""
	
	tags = ['area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input', 'isindex', 'link', 'meta', 'param']
	for n in tags:
		if tag.strip() == n:
			return True
	if tag[0] == '!':
		return True
	return False

def is_end_tag(tag):
	"""Takes tag, checks if it has a slash as first character after tag starts, if so returns True, else False"""
	
	if tag[0] == '/':
		return True
	return False

def is_header_tag(tag):
	"""Takes tag, checks if it is in header list (doesn't care about end tags), returns True or False."""
	"""Takes tag, compares to given list of empty content tags, returns True if it's in list, else False."""
	
	tags = ['head', 'body', 'h1', 'h2', 'h3','h4', 'h5', 'h6']
	for n in tags:
		if tag.strip() == n:
			return True
	return False

def is_start_tag(tag):
	"""Takes tag, returns True if it is not an empty tag and not a pre tag, else False"""
	
	if is_empty_tag(tag):
		return False
	if is_pre_tag(tag):
		return False
	if is_end_tag(tag):
		return False	
	if is_header_tag(tag):
		return False			
	return True

def is_there_end_tag(line, tag):
	"""Takes line and tag, looks for a matching end tag, returns True or False."""
	
	matching_end_tag = '/' + tag
	index_of_matching_end_tag = line.find(matching_end_tag)
	if index_of_matching_end_tag >= 0:
		return True
	return False
	

def insert_new_line(line, start_ind):
	"""Takes line and inserts new line character at index, returns line."""
	
	line = line[0:start_ind] + '\n' + line[start_ind:]
	return line

def indent(line, start_ind): #make sure indent happens before adding to tag list
	"""Takes line, adds indent at index based on current number of items in tag_list, returns line."""
	
	global tag_list
	indent = '  '
	number_indents = len(tag_list)
	for times in range(number_indents):
		line = line[:start_ind] + indent +line[start_ind:]
	return line

def both_tags_in_line(line, tag, index_after_tag):
	"""Takes line and tag, makes local tag_list, does popping on and off trick, 
	as soon as the list is empty, adds the tag to global tag list, returns index 
	after end tag. If can't find, returns -1."""
	
	global tag_list
	local_tag_list = [tag]
	new_index_after_tag = index_after_tag
	next_tag_info = get_tag(line[index_after_tag:])

	while next_tag_info != -1:
		new_index_after_tag = new_index_after_tag + next_tag_info[2]
		tag_name = next_tag_info[0]
		if tag_name[1:] == local_tag_list[-1]:
			local_tag_list.pop()
		else:
			if not is_empty_tag(tag_name):
				local_tag_list.append(next_tag_info[0])
		if len(local_tag_list) == 0:
			return new_index_after_tag
		else: 
			next_tag_info = get_tag(line[new_index_after_tag:])
	tag_list.append(tag)
	return -1

def is_in_tag_list(tag):
	"""Takes tag, compares it to global tag_list, returns True or False."""

	global tag_list
	if tag in tag_list:
			return True
	else:
		return False

def find_tag_list_index(tag):
	"""Take tag, finds its index in the global tag_list. returns index."""
	#if we get errors with finding the wrong tags, count backwards instead of forwards
	
	global tag_list
	for index in range(len(tag_list)):
		if tag_list[index] == tag:
			return index

def create_and_insert_tag(line, tag_list_index, line_index, index_after_tag): #should it just be start_ind?
	"""Takes line and tag_list_index and line_index, creates end tag for all tags after 
	tag_list_index, inserts in line at line_index. Pops those tags from tag_list. 
	Keeps track of index after tag. Returns line and index after final tag."""
	
	global tag_list
	tags_to_create = []
	for n in tag_list[tag_list_index:]:
		tags_to_create.append(n)

	end_of_line = line[index_after_tag:]
	builder_line = ''
	#run through list backwards, indent and pop as you go
	while len(tags_to_create) > 0:		
		piece_to_add = '</' + tags_to_create[-1] + '>'
		tag_list.pop() # if we have trouble lining things up, move this to before the previous line
		piece_to_add = '\n' + indent(piece_to_add, 0)
		builder_line = builder_line + piece_to_add
		tags_to_create.pop() 
	whole_line = line[:line_index] + builder_line + end_of_line
	index_after_tag = line_index + len(builder_line)
	return [whole_line, index_after_tag]


def delete_tag(line, tag, start_ind, index_after_tag):
	"""Takes line and problem end tag and start index and end index, returns line without tag."""
	
	new_line = line[:start_ind] + line[index_after_tag:]
	return new_line

def find_pre_end_tag(line):
	"""Takes a line, finds a pre end tag on that line.
	Returns the index after the pre end tag."""
	
	start_ind = line.find('/pre')
	if start_ind == -1:
		return -1
	index_after_tag = start_ind + 5
	return index_after_tag

def fix_nesting(line, tag, start_ind, index_after_tag):
	"""Takes line and problem tag and start index and end index, checks if the tag exists in global tag_list. 
	If not, deletes tag from line, if so, creates necessary tags, updating tag_list. 
	Returns line and index_after_tag."""
	
	global tag_list
	tag_name = tag[1:]
	keep_tag = is_in_tag_list(tag_name)
	if keep_tag:
		tag_list_index = find_tag_list_index(tag_name)
		line_info = create_and_insert_tag(line, tag_list_index, start_ind, index_after_tag)
		line = insert_new_line(line_info[0], line_info[1])
		index_after_tag = line_info[1] + 1
		return [line, index_after_tag]
	else:
		line = delete_tag(line, tag, start_ind, index_after_tag)
		return [line, start_ind]

def get_tag_list():
	"""Returns the global tag_list (good for testing)."""
	
	global tag_list
	return tag_list

def set_tag_list(test_list):
	"""Sets the global tag_list, for testing purposes"""
	
	global tag_list 
	tag_list = test_list

def set_need_end_pre(boolean):
	"""Sets the global need_end_pre, for testing purposes"""
	
	global need_end_pre
	need_end_pre = boolean

def get_need_end_pre():
	"""Returns the global need_end_pre, for testing purposes."""

	global need_end_pre
	return need_end_pre


"""Processing functions"""

def handle_pre_tag(line, tag, start_ind):
	"""Takes line and (pre) tag and start_ind, if tag is not the first 
	on line, adds newline and appropriate indent before. Finds end pre 
	tag, and keeps everything the same between them. return line and 
	index after end pre tag. If end pre tag not found, return indented 
	line and -1 for index and update global need_end_pre."""
	
	global need_end_pre
	if is_first_on_line(line, tag) == False:
		line = insert_new_line(line, start_ind)
		start_ind = start_ind + 1
	line = indent(line, start_ind)
	index_after_tag = find_pre_end_tag(line)
	if index_after_tag != -1:
		return [line, index_after_tag]
	need_end_pre = True
	return [line, index_after_tag]


def handle_empty_tag(line, start_ind, index_after_tag):
	"""Takes line and start_ind and index_after_tag, if it's the first tag on line,
	indent line properly. Returns line and index_after_tag."""

	if is_first_tag_in_line(line, start_ind):
		line = indent(line, 0)
		indent_tracker_line = ''
		indent_tracker_line = indent(indent_tracker_line, 0)
		index_after_tag += len(indent_tracker_line)
	return [line, index_after_tag]

def handle_missing_end_pre(line):
	"""Only needed if global need_end_pre is True. Takes the line, indents properly, searches
	for end pre tag, if found, updates need_end_pre to False and returns index_after_tag.
	If line does not contain end pre tag, just returns line and -1."""
	
	global need_end_pre
	index_after_tag = find_pre_end_tag(line)
	if index_after_tag != -1:
		need_end_pre = False
		return [line, index_after_tag]
	return [line, index_after_tag]



def handle_start_tag(line, tag, start_ind, index_after_tag):
	"""Takes line and tag and start_ind and index_after_tag, see if both tags in line, if yes, indent 
	properly before tag (keep track for index), if not place newline 
	and indent before tag(keep track for index), then return line and 
	index after tag."""

	indent_tracker_line = ''
	index_after_correct_nesting = both_tags_in_line(line, tag, index_after_tag) 
	if index_after_correct_nesting != -1:
		if is_first_tag_in_line(line, start_ind):
			line = indent(line, 0)
			indent_tracker_line = indent(indent_tracker_line, 0)
			number_of_indents = len(indent_tracker_line)
			index_after_tag = index_after_correct_nesting + number_of_indents
			return [line, index_after_tag]
		else:
			return [line, index_after_correct_nesting]

	else:
		indent_tracker_line = indent(indent_tracker_line, 0)
		indent_tracker_line = indent_tracker_line[2:]
		if is_first_tag_in_line(line, start_ind):
			if not is_first_on_line(line, tag):
				line = indent_tracker_line + line
				start_ind += len(indent_tracker_line)
				index_after_tag += len(indent_tracker_line)
		line = line[:start_ind] + indent_tracker_line + line[start_ind:]

		line = insert_new_line(line, start_ind)
		index_after_tag = index_after_tag + len(indent_tracker_line) + 1
		return [line, index_after_tag]

def handle_initial_indent(line, start_ind):
	"""Takes a line and start_ind, only if the tag being handled was the first tag in
	the line. Indents the beginning of the line appropriately and returns the line
	and the number of indents that were inserted."""
	
	indent_tracker_line2 = ''
	line = indent(line, 0)
	indent_tracker_line2 = indent(indent_tracker_line2, 0)
	number_of_indents = len(indent_tracker_line2)
	return [line, number_of_indents]



def handle_end_tag(line, tag, start_ind, index_after_tag): #should only happen if there wasn't already a matching start tag on this line
	"""Takes line and end tag and start_ind and index_after_tag, checks if it's the last thing in the global 
	tag list, if so pops from tag list. If not, goes to fix_nesting. 
	Then inserts newlines before and after tag, indents two less than 
	previously to match start tag indent, pops appropriate tags. 
	returns line and index after tag."""
	
	global tag_list
	tag_name = tag[1:]
	indent_tracker_line = ''

	if is_first_tag_in_line(line, start_ind):
		updated_info = handle_initial_indent(line, start_ind)
		line = updated_info[0]
		start_ind += updated_info[1]
		index_after_tag += updated_info[1]

	if tag_list[-1] == tag_name:
		tag_list.pop()
		#deleted insert_newline, lowered index_after_tag by 1
		indent_tracker_line = indent(indent_tracker_line, 0)
		index_after_tag = index_after_tag + len(indent_tracker_line) + 1
		line = indent(line, start_ind)
		line = insert_new_line(line, start_ind)
		if line[index_after_tag:] != '':
			line = insert_new_line(line, index_after_tag)
			index_after_tag += 1
		return [line, index_after_tag]

	else:
		line_info = fix_nesting(line, tag, start_ind, index_after_tag)
		return [line_info[0], line_info[1]]


def handle_header(line, tag, start_ind, index_after_tag):
	"""Takes line and tag and start_ind and index_after_tag, if there's anything before tag, 
	insert 2 newlines before tag properly indented, also make sure beginning of line before 
	header was properly indented (keep track of index), if it's already at 
	front, insert 1 newline before (keep track of index). 
	Will then call both_tags_in_line. if not in same line, return line and 
	index_after_tag, otherwise, returns line and index 
	that both_tags_in_line returned."""
	
	indent_tracker_line = ''
	if is_first_on_line(line, tag):
		number_of_indents = len(indent(indent_tracker_line, 0))
		line = indent(line, start_ind)
		line = insert_new_line(line, 0)
		start_ind += 1 + number_of_indents
		index_after_tag += 1 + number_of_indents
	else: 
		if is_first_tag_in_line(line, start_ind):
			line = indent(line, 0)
			number_of_indents = len(indent(indent_tracker_line, 0))
			start_ind += number_of_indents
			line = indent(line, start_ind)
			line = insert_new_line(line, start_ind)
			line = insert_new_line(line, start_ind)
			start_ind += 2 + number_of_indents
			index_after_tag += number_of_indents + number_of_indents + 2
		else:
			number_of_indents = len(indent(indent_tracker_line, 0))
			line = indent(line, start_ind)
			line = insert_new_line(line, start_ind)
			line = insert_new_line(line, start_ind)
			start_ind += 2 + number_of_indents
			index_after_tag += 2 + number_of_indents

	new_indent_tracker_line = ''
	index_after_correct_nesting = both_tags_in_line(line, tag, index_after_tag) 
	if index_after_correct_nesting != -1:
		index_after_tag = index_after_correct_nesting
	return [line, index_after_tag]
	

def process_line(line):
	"""Takes line, finds tag, determines what kind of tag it is, handles 
	is accordingly. Returns fully formatted line."""
	
	tag_info = get_tag(line)
	index_after_tag = 0
	if not need_end_pre:
		if tag_info == -1:
			line = indent(line, 0)
			return line
	while line[index_after_tag:] != '':
		"""While need end pre, must handle_missing_end_pre"""
		if need_end_pre:
			return_info = handle_missing_end_pre(line)
			line = return_info[0]
			index_after_tag = return_info[1]
			if index_after_tag == -1:
				break
			else:
				index_after_tag += return_info[1]
				if line[index_after_tag:] == '':
					break

		"""Find next tag. If no more tags in this line, returns fully formattted line."""
		tag_info = get_tag(line[index_after_tag:])
		if tag_info == -1:
			break	
		tag = tag_info[0]
		start_ind = index_after_tag + tag_info[1]
		index_after_tag = index_after_tag + tag_info[2]
	

		"""If it's a pre, handle pre tag"""
		if is_pre_tag(tag):
			return_info = handle_pre_tag(line, tag, start_ind)
			line = return_info[0]
			index_after_tag = return_info[1]

		"""If it's a header, handle header"""
		if is_header_tag(tag):
			return_info = handle_header(line, tag, start_ind, index_after_tag)
			line = return_info[0]
			index_after_tag = return_info[1]

		"""If it's an empty tag, handle empty tag"""
		if is_empty_tag(tag):
			return_info = handle_empty_tag(line, start_ind, index_after_tag)
			line = return_info[0]
			index_after_tag = return_info[1]

		"""If it's an start tag, handle start tag"""
		if is_start_tag(tag):
			return_info = handle_start_tag(line, tag, start_ind, index_after_tag)
			line = return_info[0]
			index_after_tag = return_info[1]

		"""If it's an end tag, handle end tag"""
		if is_end_tag(tag):
			return_info = handle_end_tag(line, tag, start_ind, index_after_tag)
			line = return_info[0]
			index_after_tag = return_info[1]

		"""process rest of line from index_after_tag:
		if line[index_after_tag:] == '':
			return line
		line = line[:index_after_tag] + process_line(line[index_after_tag:])"""

	return line

	

"""Main function"""

def main():

	"""Allows user to choose file to format. Counts lines for processing."""
	file_info = count_file_lines()
	counter = file_info[0]
	path = file_info[1]

	"""Makes a backup file with same name and .bak extension."""
	make_backup(path)

	"""Generates a random temp file. Opens files for processing."""
	temp_path = make_output_file_name()
	work_file = open(temp_path, 'w')
	file = open(path, 'r')

	"""Formats lines in accordance with HTML guidelines per instructions. Ignore line length."""
	counter2 = 0
	while counter2 <= counter :
		counter2 = counter2 + 1
		line = file.readline()
		line = line.strip()
		if not line: continue
		line = process_line(line) + '\n'
		work_file.write(line)
	work_file.close()

	"""Opens a new file to write the next step of formatting."""
	work_file = open(temp_path, 'r')
	work_file2 = open('post_cut.html', 'w')

	"""Cuts the already formatted lines into lines of 80 characters."""
	g = True
	while g:
		line = work_file.readline()
		if not line: break
		line = textwrap.fill(line, 80) + '\n'
		work_file2.write(line)

	work_file.close()
	work_file2.close()

	"""Opens original file to overwrite the final step of formatting."""
	work_file2 = open('post_cut.html', 'r')
	work_file3 = open(path, 'w')

	"""Reads in the formatted, cut lines, and for all lines that were cut, adjusts the indents
	to match the indent of the line above. Does not go back to reprocess after having cut the lines."""
	a = True
	remember_indent = 0
	while a:
		line = work_file2.readline()
		if not line: break
		this_indent = len(line) - len(line.lstrip(' '))
		if this_indent > 0:
			remember_indent = this_indent
		else:
			line = make_whitespace(remember_indent) + line
		work_file3.write(line)

	work_file2.close()
	work_file3.close()

	"""Deletes the temporary files from the system."""
	os.remove('post_cut.html')
	os.remove(temp_path)


if __name__ == "__main__":
    main()	

