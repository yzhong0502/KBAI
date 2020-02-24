# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops
import operator
import math
from functools import reduce
import numpy as np

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.answers = []
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        # check problem type
        if problem.problemType == '2x2':
            self.answers = ['1', '2', '3', '4', '5', '6']
        else:
            self.answers = ['1', '2', '3', '4', '5', '6', '7', '8']
        # check if the problem has verbal representation
        if problem.hasVisual:
            # check the figures one by one depending on its problem type
            # get Ravens objects from each figure
            current_ans = '-1'
            current_score = 0
            if problem.problemType == '2x2':
                # A B
                # C ?
                A = problem.figures['A']
                B = problem.figures['B']
                C = problem.figures['C']
                im_A = Image.open(A.visualFilename)
                im_B = Image.open(B.visualFilename)
                im_C = Image.open(C.visualFilename)
                current_diff = float("inf")
                choice = 0
                for opt in self.answers:
                    option = problem.figures[opt]
                    im_opt = Image.open(option.visualFilename)
                    score = self.compute_score(im_A, im_B, im_C, im_opt)
                    if score > current_score:
                        current_score = score
                        current_ans = opt
                    if score == 0:
                        d_AB = self.compute_diff(im_A, im_B)
                        d_co = self.compute_diff(im_C, im_opt)
                        d = abs(d_AB-d_co)
                        if d < current_diff:
                            current_diff = d
                            choice = opt
                if current_ans == -1:
                    current_ans = choice
                return int(current_ans)
            else: # 3x3
                # A B C
                # D E F
                # G H ?
                A = problem.figures['A']
                B = problem.figures['B']
                C = problem.figures['C']
                D = problem.figures['D']
                E = problem.figures['E']
                F = problem.figures['F']
                G = problem.figures['G']
                H = problem.figures['H']
        return -1

    # exclude options by number of objects
    def exclude_by_num(self, problem):
        if problem.problemType == '2x2':
            num_A = len(problem.figures['A'].objects)
            num_B = len(problem.figures['B'].objects)
            num_C = len(problem.figures['C'].objects)
            nums_ans = 0
            k = num_A - num_B
            if k == 0:
                nums_ans = num_C
            else:
                nums_ans = num_C-k
                '''
                if k > 0:
                    if  num_B != 0:
                        d = num_A//num_B
                        if d == num_A/num_B and num_C//d == num_C/d:
                            nums_ans.append(num_C//d)
                '''
            to_del = []
            for i in range(len(self.answers)):
                option = self.answers[i]
                num_opt = len(problem.figures[option].objects)
                if num_opt != nums_ans:
                    to_del.append(option)
            for d in to_del:
                for j in range(len(self.answers)):
                    if d == self.answers[j]:
                        del self.answers[j]
                        break
        # case 3x3
        else:
            num_A = len(problem.figures['A'].objects)
            num_B = len(problem.figures['B'].objects)
            num_C = len(problem.figures['C'].objects)
            num_D = len(problem.figures['D'].objects)
            num_E = len(problem.figures['E'].objects)
            num_F = len(problem.figures['F'].objects)
            num_G = len(problem.figures['G'].objects)
            num_H = len(problem.figures['H'].objects)
            nums_ans = []
            if num_A == num_B and num_B == num_C and num_A == num_D and num_D == num_G:
                nums_ans.append(num_A)
            elif num_D - num_A == num_G - num_D and num_D != num_A:
                nums_ans.append(2*num_F-num_C)
            elif num_B - num_A == num_C - num_B and num_B != num_A:
                nums_ans.append(2*num_H-num_G)
            elif num_B == num_F and num_D == num_H and num_A == num_E and num_A not in nums_ans:
                nums_ans.append(num_A)
            elif num_A + num_B + num_C == num_D + num_E + num_F and num_A != num_D:
                nums_ans.append(num_A+num_B+num_C-num_G-num_H)
            elif num_C == num_A+num_B and num_F == num_D+num_E:
                nums_ans.append(num_G+num_H)

            to_del = []
            for i in range(len(self.answers)):
                option = self.answers[i]
                num_opt = len(problem.figures[option].objects)
                if num_opt not in nums_ans:
                    to_del.append(option)
            for d in to_del:
                for j in range(len(self.answers)):
                    if d == self.answers[j]:
                        del self.answers[j]
                        break

    # pair objects from different figure using the same key. The name is
    # based on dic_1 so the key of dic_2 will be updated
    def compute_score(self, A, B, C, option):
        score = 0
        if self.check_same(A, B) and self.check_same(C, option):
            score += 2
        if self.check_same(A, C) and self.check_same(B, option):
            score += 2
        a = self.check_rotate(A, B)
        if a>0 and a == self.check_rotate(C, option):
            score += 1
        b = self.check_rotate(A, C)
        if b>0 and b == self.check_rotate(B, option):
            score += 1
        c = self.check_mirror(A, B)
        if c>0 and c == self.check_mirror(C, option):
            score += 1
        d = self.check_mirror(A, C)
        if d>0 and d == self.check_mirror(B, option):
            score += 1
        return score

    def compute_score_3(self, A, B, C, D, E, F, G, H, option):
        score = 0
        if len(C.objects) > len(B.objects) > len(A.objects):
            pairs_cb = self.pair_objects(C, B)
            pairs_ba = self.pair_objects(B, A)
            for name_c in pairs_cb:
                name_b = pairs_cb[name_c]

        pairs_ab = self.pair_objects(A, B)
        pairs_bc = self.pair_objects(B, C)
        pairs_ad = self.pair_objects(A, D)
        pairs_dg = self.pair_objects(D, G)
        pairs_gh = self.pair_objects(G, H)
        pairs_ho = self.pair_objects(H, option)
        for name_a in pairs_ab:
            obj_a = A.objects[name_a]
            name_b = pairs_ab[name_a]
            if name_c=='':
                pass
        return score


    # Link objects from f2 to f1
    def pair_objects(self, f1, f2): # return obj_name_1:obj_name_2 pairs. f1>=f2?
        # f1 should have equal or more objects than f2?
        # return directly if there is only one object in each figure
        pairs = {}  # obj_1:obj_2
        if len(f1.objects) == len(f2.objects) == 1:
            pairs[list(f1.objects.keys())[0]] = list(f2.objects.keys())[0]
        # link the objects which have the most same attributes

        if len(f1.objects)<=len(f2.objects):
            objects_2 = f2.objects.copy()
            for obj_1 in f1.objects:
                Obj_1 = f1.objects[obj_1]
                n = 0 # num of same attributes
                most = 0
                most_2 = '' # name of obj_2 which has the most same attributes with obj_1
                if len(objects_2)==0:
                    print('error')
                if len(objects_2)==1:
                    most_2 = list(objects_2.keys())[0]
                else:
                    for obj_2 in objects_2:
                        Obj_2 = objects_2[obj_2]
                        for key in Obj_1.attributes:
                            if key not in Obj_2.attributes:
                                continue
                            elif Obj_1.attributes[key] == Obj_2.attributes[key]:
                                n += 1
                        if n>most:
                            most = n
                            most_2 = obj_2
                pairs[obj_1] = most_2
                if most_2 != '':
                    del objects_2[most_2]
        else:
            re_pairs = {} # obj_2:obj_1
            objects_1 = f1.objects.copy()
            for obj_2 in f2.objects:
                Obj_2 = f2.objects[obj_2]
                n = 0 # match score - next round consider
                most = 0
                most_1 = '' # name of obj_2 which has the most same attributes with obj_1
                if len(objects_1)==0:
                    print('error')
                if len(objects_1)==1:
                    most_1 = list(objects_1.keys())[0]
                else:
                    for obj_1 in objects_1:
                        Obj_1 = objects_1[obj_1]
                        for key in Obj_1.attributes:
                            if key not in Obj_2.attributes:
                                continue
                            elif Obj_1.attributes[key] == Obj_2.attributes[key]:
                                n += 1
                        if n>most:
                            most = n
                            most_1 = obj_1
                re_pairs[obj_2] = most_1
            pairs = {value: key for key, value in re_pairs.items()}
            names = list(pairs.keys())
            for name_1 in list(f1.objects.keys()):
                # name_1 in f1 is deleted in f2
                if name_1 not in names:
                    pairs[name_1]=''
        return pairs


    def compute_diff(self, im_1, im_2):
        h1 = im_1.histogram()
        h2 = im_2.histogram()
        diff = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return diff

    # compare images based on visual file
    def check_same(self, im_1, im_2):
        # 1 check same
        diff = ImageChops.difference(im_1, im_2)
        if diff.getbbox() is None:
            return True  # same
        else:
            return False

    def check_rotate(self, im_1, im_2):
        # 2 check rotate
        degree = [90, 180, 270]
        for d in degree:
            new_1 = im_1.rotate(d)
            if self.check_same(new_1, im_2):
                return d  # rotate
        return -1 # no rotate

    def check_mirror(self, im_1, im_2):
        # 2 check mirror
        new_1 = im_1.transpose(Image.FLIP_LEFT_RIGHT)
        if self.check_same(new_1, im_2):
            return 1  # flip left right
        new_1 = im_1.transpose(Image.FLIP_TOP_BOTTOM)
        if self.check_same(new_1, im_2):
            return 2  # flip top bottom
        return -1  # no mirror


