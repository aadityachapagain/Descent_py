import itertools, re
import pyperclip, freqAnalysis, detectEnglish
import vigenere_cipher as cipher

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False # if set to True, program doesn't print attempts
NUM_MOST_FREQ_LETTERS = 4 # attempts this many letters per subkey
MAX_KEY_LENGTH = 16 # will not attempt keys longer than this
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
    ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi,
    lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz
    hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg
    jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk
    qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum.
    Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg
    (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav
    wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o
    iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq
    pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms
    umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz
    cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi
    1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg,
    ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe
    avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at
    hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce
    Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a
    tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn
    wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm
    tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz
    1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn
    avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk
    jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt
    uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby
    gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa
    at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd
    yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""

    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copyig hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print(' failed to hack the ecryption ')


def findRepeatSequenceSpacings(message):
    # goes through the message  and finds any 3 to 5 letter sequences that are repeated . Returns a dict with keys
    # of the sequence and values of a list of spacing (num of letter between the repeats ).

    # use regular expression to remove non letters from the message
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message.
    seqSpacing = {} # keys are sequence , values are list of int spacings
    for seqLen in range(3,6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is , and store it in seq
            seq = message[seqStart :seqStart+seqLen]

            # Look for this seq for rest of the message
            for i in range(seqStart + seqLen,len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence
                    if seq not in seqSpacing:
                        seqSpacing[seq] = []

                    # Append the spacing distance between the repeated
                    # sequence  and the original  sequence.
                    seqSpacing[seq].append(i - seqStart)

    return seqSpacing


def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1.

    if num < 2 :
        return [] # number less than 2  has no usefull factors

    factors = [] # list of factors found

    # when finding factors you only need to check the integers up to
    # MAX_KEY_LENGTH
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i  == 0:
            factors.append(i)
            factors.append(int(num/i))

        if 1 in factors:
            factors.remove(1)
        return list(set(factors))



def getItemAtIndexOne(x):
    return x[1]


def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors.
    factorsCount = {} # key is a factors , value is how often if  occurs

    # seqFactors keys are sequence, values are lists of factors of the spacing

    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorsCount:
                factorsCount[factor] = 0
            factorsCount[factor] += 1

    # second, put the factor and its count into a tuple, and make a list of these
    # of tuples so we can sort them
    factorsByCount = []
    for factor in factorsCount:
        # exclude factors larger than MAX_KEY_LENGTH
        if factor  <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorsCount[factor]))

    # sort the list by the factor count.
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount

def kasiskiExamination(ciphertext):
    # find out the sequence of 3 to 5 letters that occur multiple times in the ciphertext.
    repeatedSeqSpacings = findRepeatSequenceSpacings(ciphertext)

    # see getMostCommonFactors() for a description of seqFactors.
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # see getMostCommonFactors() for a descrition of factorsByCount.
    factorsByCount = getMostCommonFactors(seqFactors)

    # now we extreact the factors from factorsByCount and put them in allLikelyLengths so
    # that they are easier to use later.
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths

def getNthSubKeysLetters(n,keyLength,message):
    # returns every Nth letter for each keyLength set of  letters in text.

    # use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('',message)
    i  = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # determine the most likely letter for each letter in the key.
    ciphertextUp = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # these inner lists are the freqScores lists.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubKeysLetters(nth,mostLikelyKeyLength,ciphertextUp)

        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = cipher.decryptMessage(possibleKey,nthLetters)

            keyAndFreqMatchTuple = (possibleKey,freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)

            # sort by match score
        freqScores.sort(key=getItemAtIndexOne, reverse = True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print('possible letters for letter {0} of the key:'.format(i+1))

            for freqScore in allFreqScores[i]:
                print('{}'.format(freqScore[0]), end='')
            print()


    