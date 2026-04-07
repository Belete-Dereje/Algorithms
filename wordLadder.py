from collections import deque

def word_ladder(start, goal, word_list):
    word_set = set(word_list)
    queue = deque([(start, [start])])

    while queue:
        word, path = queue.popleft()

        if word == goal:
            return path

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]

                if new_word in word_set:
                    word_set.remove(new_word)
                    queue.append((new_word, path + [new_word]))

    return None

words = ["hot","dot","dog","lot","log","cog"]
print(word_ladder("hit", "cog", words))