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
from PIL import ImageOps
from PIL import ImageEnhance
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
        self.threshold = 461  # 461

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
                # invert black/white and convert to grey mode
                im_A = self.open_pre(A)
                im_B = self.open_pre(B)
                im_C = self.open_pre(C)


                for opt in self.answers:
                    option = problem.figures[opt]
                    im_opt = self.open_pre(option)
                    score = self.compute_score(im_A, im_B, im_C, im_opt)
                    if score > current_score:
                        current_score = score
                        current_ans = opt
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
                im_A = self.open_pre(A)
                im_B = self.open_pre(B)
                im_C = self.open_pre(C)
                im_D = self.open_pre(D)
                im_E = self.open_pre(E)
                im_F = self.open_pre(F)
                im_G = self.open_pre(G)
                im_H = self.open_pre(H)

                print(problem.name)

                # deal with C-04, C-06 & C-10
                a = im_A.getbbox()
                if a == None:
                    a = (0, 0, 0, 0)
                b = im_B.getbbox()
                c = im_C.getbbox()
                d = im_D.getbbox()
                e = im_E.getbbox()
                f = im_F.getbbox()
                g = im_G.getbbox()
                h = im_H.getbbox()
                if problem.name == "Basic Problem C-10":
                    print(a)
                    print(b)
                    print(c)
                    print(d)
                    print(e)
                    print(f)
                    print(g)
                    print(h)

                x,y = 0,0
                if b != None and c != None and d != None and e != None and f != None and g != None and h != None:
                    ax = a[2]-a[0]
                    ay = a[3]-a[1]
                    bx = b[2] - b[0]
                    by = b[3] - b[1]
                    cx = c[2] - c[0]
                    cy = c[3] - c[1]
                    dx = d[2] - d[0]
                    dy = d[3] - d[1]
                    ex = e[2] - e[0]
                    ey = e[3] - e[1]
                    fx = f[2] - f[0]
                    fy = f[3] - f[1]
                    gx = g[2] - g[0]
                    gy = g[3] - g[1]
                    hx = h[2] - h[0]
                    hy = h[3] - h[1]
                    if abs(by-ay)<3 and abs(cy-by)<3 and ax!=bx!=cx:
                        if abs(dx-ax)<3 and abs(gx-dx)<3 and ay!=dy!=gy:
                            if abs(dy-ey)<3 and abs(fy-ey)<3 and dx!=ex!=fx:
                                if abs(bx-ex)<3 and abs(hx-ex)<3 and by!=ey!=hy:
                                    if abs(gy-hy)<3 and gx!=hx:
                                        if abs(cx-fx)<3 and cy!=fy:
                                            x = cx
                                            y = gy

                for opt in self.answers:
                    option = problem.figures[opt]
                    im_opt = self.open_pre(option)
                    score = self.compute_score(im_A, im_C, im_G, im_opt)

                    # C-04, C-06 & C-10
                    if x!=0 and y!=0:
                        o = im_opt.getbbox()
                        if opt == '7':
                            print(o)
                        ox = o[2]-o[0]
                        oy = o[3]-o[1]
                        if abs(ox-x)<5 and abs(oy-y)<5:
                            score += 1

                    if score > current_score:
                        current_score = score
                        current_ans = opt
                    print(opt, ": ", score)
                return int(current_ans)

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
        same_score = 10
        mirror_score = 8
        rotate_score = 6
        if self.check_same(A, B) and self.check_same(C, option):
            return same_score
        if self.check_same(A, C) and self.check_same(B, option):
            return same_score
        c = self.check_mirror(A, B)
        if c is not None:
            cc = self.check_mirror(C, option)
            if cc is not None and c == cc:
                return mirror_score
        d = self.check_mirror(A, C)
        if d is not None:
            dd = self.check_mirror(B, option)
            if dd is not None and d == dd:
                return mirror_score
        a = self.check_rotate(A, B)
        if a is not None:
            aa = self.check_rotate(C, option)
            if aa is not None and a == aa:
                return rotate_score
        b = self.check_rotate(A, C)
        if b is not None:
            bb = self.check_rotate(B, option)
            if bb is not None and b == bb:
                return rotate_score
        return 0



    # open and pre deal with image
    @staticmethod
    def open_pre(im):
        # invert black/white and convert to grey mode
        im_grey = Image.open(im.visualFilename).convert('L')

        enh_con = ImageEnhance.Contrast(im_grey)
        contrast = 1.5
        img_contrasted = enh_con.enhance(contrast)

        im_r = ImageOps.invert(img_contrasted)
        nd = Agent.im_to_np(im_r)
        im_a = Image.fromarray(np.uint8(nd))
        return im_a

    @staticmethod
    def im_to_np(im):
        i = np.array(im)
        # i[i >= 10] = 255  # white
        i[i < 255] = 0  # black
        return i

    @staticmethod
    def compute_diff(im_1, im_2):
        i_1 = Agent.im_to_np(im_1)
        i_2 = Agent.im_to_np(im_2)
        # diff = np.linalg.norm(i_1 - i_2)  # Euclidean distance
        # diff = np.sum(abs(i_1-i_2) > 60)
        diff = np.sum(i_1!=i_2)
        return diff

    # compare images based on visual file
    @staticmethod
    def check_same(im_1, im_2):
        # 1 check same
        diff = ImageChops.difference(im_1, im_2).getbbox()
        if diff is None:
            return True
        else:
            return False
        '''
        if self.compute_diff(im_1, im_2) < self.threshold:
            return True
        return False
        '''

    def check_rotate(self, im_1, im_2):
        # 2 check rotate
        degree = [45, 90, 135, 180, 225, 270]
        for d in degree:
            new_1 = im_1.copy()
            new_1 = new_1.rotate(d)
            if self.compute_diff(new_1, im_2) < self.threshold:
                return d  # rotate
        return  # no rotate

    def check_mirror(self, im_1, im_2):
        # 2 check mirror
        new_1 = im_1.copy()
        new_1 = new_1.transpose(Image.FLIP_LEFT_RIGHT)
        if self.compute_diff(new_1, im_2) < self.threshold:
            return 'LR'  # flip left right
        new_11 = im_1.copy()
        new_11 = new_11.transpose(Image.FLIP_TOP_BOTTOM)
        if self.compute_diff(new_11, im_2) < self.threshold:
            return 'TB'  # flip top bottom
        return  # no mirror

    # try PIL.image.paste or numpy.roll to detect offset

