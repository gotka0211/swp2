import pickle

dbfilename = 'assignment3.dat'

def readScoreDB(): #실행시 데이터파일을 읽어들여 scoredb리스트에 데이터를 사전형식으로 저장합니다.
    try:
        fH = open(dbfilename,'rb')
    except FileNotFoundError as e:
        print('New DB: ', dbfilename)
        return[] 
    scdb=[]
    try:
        scdb = pickle.load(fH)
    except:
        print('Empty DB: ',dbfilename)
    else:
        print('Open DB: ',dbfilename)
    fH.close()
    return scdb

def setScoreDB(scdb): #처음에 불러오는 ScoreDB의 Age와 Score의 값이 String일때 정수로 변환합니다.
    for i in scdb:
        for j in i:
            try: #항상 i[j]를 정수로 바꾸려 시도합니다.
                i[j] = int(i[j])
            except: #그러나 해당값이 문자열일 경우 그냥 넘깁니다.
                pass            

def writeScoreDB(scdb): #성적관리 프로그램 종료시 dbfilename에 Scoredb안의 데이터를 저장합니다.
    fH = open(dbfilename, 'wb')    
    pickle.dump(scdb, fH)
    fH.close()
    print('Data saved...')

def doScoreDB(scdb): #성적관리 프로그램
    while(True):
        inputstr = (input('Score DB > '))
        if inputstr == '': continue
        parse = inputstr.split(' ')
        
        if parse[0] == 'add': #새로운 사람의 정보를 ScoreDB에 추가합니다.
            try:
                record = {'Name':parse[1],'Age':int(parse[2]),'Score': int(parse[3])}
                scdb += [record]
                print('New data: Age:{}, Name:{}, Score:{}'.format(parse[2],parse[1],parse[3]))
            except IndexError: #인자를 충분히 기입하지 않았을 경우
                print('Insufficient information!')
                print('  #\'add\' requires : Name, Age, Score')
            except ValueError: #나이와 점수에 숫자가 아닌 수를 넣었을 경우 
                print('Invalid data type!')
                print('  #Age & Score must be Integer')
            
        elif parse[0] == 'del': #해당이름을 가진 사람의 정보를 모두 삭제합니다.
            try:
                dellist=[] 
                for p in scdb: #del할 사람이 리스트에 있는지 판별하여  
                    if p['Name'] == parse[1]:
                        dellist.append(p) #해당 이름의 사람의 수만큼 dellist가 채워집니다.
                if dellist: #그러면 그 수만큼 scdb에서 del 작업을 수행하여 해당이름을 가진 모든 사람의 정보를 삭제합니다.  
                    for p in dellist: 
                        scdb.remove(p)
                    print(parse[1],': deleted Successfully')
                else: #해당 사람이 리스트에 없는 경우
                    print(parse[1],': not in the ScoreDB! Try again!')                 
            except IndexError: #인자를 충분히 기입하지 않았을 경우
                print('Insufficient information!')
                print('  #\'del\' requires: Name')                
                
        elif parse[0] == 'show': #원하는 방식으로 정렬이 된 데이터를 화면에 출력합니다.
            try:
                sortKey = 'Name' if len(parse) == 1 else parse[1]
                showScoreDB(scdb, sortKey)
            except KeyError: #없는 key를 통해 데이터에 접근하려는 경우 
                print('Wrong key to access!')
                print('  #\'show\' requires: Age or Name or Score')
            
        elif parse[0] == 'find': #원하는 사람의 정보를 열람합니다. 동명이인은 등록순으로.
            exist=False
            try:
                for p in scdb: #리스트를 훑으면서 해당 이름을 가진 사람의 정보를 출력합니다.
                    if parse[1] in p.values(): 
                        exist=True
                        for attr in sorted(p):                    
                            print('{}={}'.format(attr,p[attr]),end=' ')
                        print()
                if not exist: #해당 사람이 리스트에 없는 경우 
                    print(parse[1],': not in the ScoreDB! Try again')
            except IndexError: #충분한 인자를 기입하지 않았을 경우 
                print('Insufficient information!')
                print('  #\'find\' requires: Name')
                    
        elif parse[0] == 'inc': #원하는 사람의 점수를 수정합니다. 
            exist=False
            try:
                for p in scdb: 
                    if parse[1] in p.values():
                        exist=True
                        p['Score'] += int(parse[2])
                if exist:
                    print('All {}\'s Scores were changed by {}'.format(parse[1],parse[2]))
                else: #해당 사람이 리스트에 없는 경우 
                    print(parse[1],': not in the ScoreDB! Try again')
            except IndexError: #충분한 인자를 기입하지 않았을 경우 
                print('Insufficient information!')
                print('  #\'inc\' requires: Name, Amount')
            except ValueError: #amount에 정수가 아닌 문자를 적었을 경우 
                print('Invalid data type!')
                print('  #Amount must be Integer')
                    
        elif parse[0] == 'quit': #프로그램을 종료합니다.
            print('Bye~')
            break
        
        else: #잘못된 명령어 입력시 오류메세지와 사용가능한 명령어들을 보여줍니다.
            print('Invalid command: '+parse[0])
            print('  #Valid instructions: add, show, find, inc, quit')

def showScoreDB(scdb,keyname): #keyname을 기준으로 데이터를 정렬하여 화면에 출력합니다.
    for p in sorted(scdb,key=lambda person: person[keyname]):
        for attr in sorted(p):
            print('{}={}'.format(attr,p[attr]),end=' ')
        print()

#실행     
scoredb = readScoreDB()
setScoreDB(scoredb) #프로그램 실행전 데이터 셋팅
doScoreDB(scoredb) #프로그램 실행 
writeScoreDB(scoredb) #프로그램이 종료되면 현재 데이터를 파일로 저장합니다.
    
