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
#from PIL import Image
#import numpy

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
    def Solve(self,problem):
        # check problem type
        if problem.problemType == '2x2':
            self.answers = ['1', '2', '3', '4', '5', '6']
        else:
            self.answers = ['1', '2', '3', '4', '5', '6', '7', '8']
        # check if the problem has verbal representation
        if problem.hasVerbal:

            # first using exclusive method to eliminate the answers that are obviously wrong.
            self.exclude_by_num(problem)
            if len(self.answers) == 0:
                return -1
            if len(self.answers) == 1:
                return int(self.answers[0])

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
                for opt in self.answers:
                    option = problem.figures[opt]
                    if len(A.objects)>=len(B.objects):
                        score = self.compute_score(A, B, C, option)
                    else:
                        score = self.compute_score(B, A, option, C)
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
                for opt in self.answers:
                    option = problem.figures[opt]
                    if len(A.objects) >= len(C.objects):
                        score = self.compute_score(A, C, G, option) # treat 3X3 as 2X2
                    else:
                        score = self.compute_score(C, A, option, G)
                    if score > current_score:
                        current_score = score
                        current_ans = opt
                return int(current_ans)
        else: # only has visual representation
            pass # need to be coded later
        return -1

    # exclude options by number of objects
    def exclude_by_num(self, problem):
        if problem.problemType == '2x2':
            num_A = len(problem.figures['A'].objects)
            num_B = len(problem.figures['B'].objects)
            num_C = len(problem.figures['C'].objects)
            nums_ans = []
            k = num_A - num_B
            if k == 0:
                nums_ans = [num_C]
            else:
                nums_ans.append(num_C-k)
                if k > 0:
                    if  num_B != 0:
                        d = num_A//num_B
                        if d == num_A/num_B and num_C//d == num_C/d:
                            nums_ans.append(num_C//d)
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
    def compute_score(self, A, B, C, option):# A>=B, C>=option
        score = 0
        pairs_ab = self.pair_objects(A, B)
        pairs_co = self.pair_objects(C, option)
        pairs_ac = self.pair_objects(A, C)
        for name_a in pairs_ab:
            obj_a = A.objects[name_a]
            name_b = pairs_ab[name_a]
            name_c = pairs_ac[name_a]
            if name_c == '':
                return score
            name_o = pairs_co[name_c]
            # obj_a is deleted in B
            if name_b == '':
                if name_c!='':
                    # obj_a is deleted in b so does option
                    if name_o=='':
                        score+=1
                    # not deleted in option
                    else:
                        score-=5
            if name_b != '':
                obj_b = B.objects[name_b]
                obj_c = C.objects[name_c]
                if name_o=='':
                    score-=5
                else:
                    obj_opt = option.objects[name_o]
                    for key in obj_a.attributes:
                        # attributes that not change weight 5
                        if key not in obj_c.attributes or key not in obj_b.attributes or key not in obj_opt.attributes:
                            continue

                        if obj_a.attributes[key] == obj_b.attributes[key] and obj_c.attributes[key] == obj_opt.attributes[key]:
                            score += 5
                        if obj_a.attributes[key] != obj_b.attributes[key] and obj_a.attributes[key] == obj_c.attributes[key] and obj_b.attributes[key] == obj_opt.attributes[key]:
                            score += 1
        '''
        if len(A.objects) == 1 and len(B.objects) == 1 and len(A.objects) == 1:
            # no need to pair objects
            obj_a = list(A.objects.values())[0]
            obj_b = list(B.objects.values())[0]
            obj_c = list(C.objects.values())[0]
            obj_opt = list(option.objects.values())[0]
            for key in obj_a.attributes:
                # attributes that not change weight 5
                if obj_a.attributes[key] == obj_b.attributes[key] and obj_c.attributes[key] == obj_opt.attributes[key]:
                    score += 5
                if obj_a.attributes[key] != obj_b.attributes[key] and obj_a.attributes[key] == obj_c.attributes[key] and obj_b.attributes[key] == obj_opt.attributes[key]:
                    score += 1
        '''
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
                                # next round uncomment
                                # if key == 'shape': n += 5 else:
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
                                # next round uncomment
                                # if key == 'shape': n += 5 else:
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



