#?/usr/beqin/env python
from pymongo import MongoClient

#Given a set of movie reviews, this will look at each word in the review, and check to see
#if the words are "positive" or "negative." If the final review score is a positive number
#then the review we be clasified as positive. Otherwise, it will be considered a negative
#review. 

#Create a conecction
client = MongoClient()
db = client.cs336

collectionSplit =  db.unlabel_review_after_splitting
collectionFull = db.unlabel_review


cursor = collectionSplit.find({}, {'id': 1, 'review': 1})       #Find all reviews and ID's
positive = set(["absolutely","adorable","accepted","acclaimed","accomplish","accomplishment","achievement","action",
                "active","admire","adventure","affirmative","affluent","agree","agreeable","amazing","angelic","appealing",
                "approve","aptitude","attractive","awesome","beaming","beautiful","believe","bliss","bountiful","bounty",
                "brave","bravo","brilliant","bubbly","calm","celebrated","certain","champ","champion","charming","cheery",
                "choice","classic","classical","clean","commend","composed","congratulation","constant","cool","courageous",
                "creative","cute","dazzling","delight","delightful","distinguished","divine","earnest","easy","ecstatic",
                "effective","effervescent","efficient","effortless","electrifying","elegant","enchanting","encouraging",
                "endorsed","energetic","energized","engaging","enthusiastic","essential","esteemed","ethical","excellent",
                "exciting","exquisite","fabulous","fair","familiar","famous","fantastic","favorable","fetching","fine","fitting",
                "flourishing","fortunate","free","fresh","friendly","fun","funny","generous","genius","genuine","giving",
                "glamorous","glowing","good","gorgeous","graceful","great","green","grin","growing","happy","harmonious",
                "healing","healthy","hearty","heavenly","honest","honorable","honored","hug","idea","ideal","imaginative",
                "imagine","impressive","independent","innovate","innovative","instant","instantaneous","instinctive","intuitive",
                "intellectual","intelligent","inventive","jovial","joy","jubilant","keen","kind","knowing","knowledgeable",
                "laugh","light","learned","lively","lovely","lucid","lucky","luminous","marvelous","masterful","merit",
                "meritorious","miraculous","motivating","moving","natural","nice","novel","now","nurturing","nutritious",
                "okay","one","open","optimistic","paradise","perfect","phenomenal","pleasurable","plentiful","pleasant",
                "poised","polished","popular","positive","powerful","prepared","pretty","principled","productive","progress",
                "prominent","protected","proud","quality","quick","quiet","ready","reassuring","refined","refreshing","rejoice",
                "reliable","remarkable","resounding","respected","restored","reward","rewarding","right","robust","safe",
                "satisfactory","secure","seemly","simple","skilled","skillful","smile","soulful","sparkling","special","spirited",
                "spiritual","stirring","stupendous","stunning","success","successful","sunny","super","superb","supporting",
                "surprising","terrific","thorough","thrilling","thriving","tops","tranquil","transforming","transformative",
                "trusting","truthful","unreal","unwavering","up","upbeat","upright","upstanding","valued","vibrant","victorious",
                "victory","vigorous","virtuous","vital","vivacious","wealthy","welcome","well","whole","wholesome","willing",
                "wonderful","wondrous","worthy","wow","yes","yummyzea","zealous"])

neg = set(["abysmal","adverse","alarming","angry","annoy","anxious","apathy","appalling","atrocious","awful","bad",
                "banal","barbed","belligerent","bemoan","beneath","boring","brokencallous","can't","clumsy","coarse","cold",
                "cold-hearted","collapse","confused","contradictory","contrary","corrosive","corrupt","crazy","creepy",
                "criminal","cruel","cry","cutting","callous","can't","clumsy","coarse","cold","cold-hearted","collapse",
                "confused","contradictory","contrary","corrosive","corrupt","crazy","creepy","criminal","cruel","cry",
                "cutting","dead","decaying","damage","damaging","dastardly","deplorable","depressed","deprived","deformed",
                "deny","despicable","detrimental","dirty","disease","disgusting","disheveled","dishonest","dishonorable",
                "dismal","distress","don't","dreadful","dreary","enraged","eroding","evil","fail","faulty","fear","feeble",
                "fight","filthy","foul","frighten","frightful","gawky","ghastly","grave","greed","grim","grimace","gross",
                "grotesque","gruesome","guilty","haggard","hard","hard-hearted","harmful","hate","hideous","homely","horrendous",
                "horrible","hostile","hurt","hurtful","icky","ignore","ignorant","ill","immature","imperfect","impossible",
                "inane","inelegant","infernal","injure","injurious","insane","insidious","insipid","jealous","junky","lose",
                "lousy","lumpy","malicious","mean","menacing","messy","misshapen","missing","misunderstood","moan","moldy",
                "monstrous","naive","nasty","naughty","negate","negative","never","no","nobody","nondescript","nonsense","not",
                "noxious","objectionable","odious","offensive","old","oppressive","pain","perturb","pessimistic","petty","plain",
                "poisonous","poor","prejudice","questionable","quirk","reptilian","repulsive","revenge","rocky","rotten","rude",
                "ruthless","sad","savage","scare","scary","scream","severe","shoddy","shocking","sick","sickening","sinister",
                "slimy","smelly","sobbing","sorry","spiteful","sticky","stinky","stormy","stressful","stuck","stupid","substandard",
                "suspect","suspicious","tense","terrible","terrifying","threatening","ugly","undermine","unfair","unfavorable",
                "unhappy","unhealthy","unjust","unlucky","unpleasant","upset","unsatisfactory","unsightly","untoward","unwanted",
                "unwelcome","unwieldy","unwise","upset","vice","vicious","vile","villainous","vindictive","wary","weary","woeful",
                "worthless","wound","yell","yucky","zero",])

#Main Loop:
JSONdata = []                                                   #Create a List to hold the JSON data
for document in cursor:                                         #For each document in U_R_after_splitting
    thisRevScore = 0                                            #Give this documents reveiw a score of 0
    thisID = document["id"]                                     #Get the documents ID
    
    cursor2 = collectionFull.find({'id': document["id"]})       #Pass this ID to the unspit reviews
    theFullRev = ""
    for doc in cursor2:
        theFullRev = doc["review"].encode("utf-8")              #Get the unsplit review....stupid Unicode.
        
    dic = document["review"]                                    #Create a dictionary containing the words and counts
    for i in range(0, len(dic)):                                #Loop through each word and count
        wordCount = dic[i]["count"]
        word = dic[i]["word"]
        if(word in positive):                                   #See if this word is in the positive set
            thisRevScore += (1 * wordCount)
        elif(word in neg):                                      #If not check if it's in the negative set
            thisRevScore -= (1 * wordCount)
    category = ""
    if(thisRevScore >= 0):                                      #Assign the review category based on review score
        category = "Positive"
    else:
        category = "Negative"                                   #Could now append category:Pos/Neg to unsplit if you wanted,
                                                                #but I didnt want to mess with the original JSON files.  
    finalString = "{id: %s , review: %s, category: %s}" % (thisID, theFullRev.decode("utf-8"), category)
    JSONdata.append(finalString)                                #Add the JSON formated string to the data list.
                                                                   
for i in range(0, len(JSONdata)):                               #Output the JSON strings if you want to view them.
    print JSONdata[i].encode("utf-8")  
    print "\n"
    
#Jason Schwartz aka JSON Schwartz
#CS336 11/20/15
