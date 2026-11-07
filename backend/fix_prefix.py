import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the dynamic world closing
marker = '        ]),\n    ]\n)\n\n# ═══════════════════════════════════════════════════════════════\n# WORLD 9: Tree Grove (trees)'
if marker in content:
    prefix_town = '''        _make_town("prefix", "Prefix Plains", "🧮", "Running totals let you answer range queries instantly.", 2, "Cumulative Sums", ["algorithms.prefix-sum"], ["prefix-sum", "range-sum", "running-total"], [
            _level("ps-1","The Running Total","🧮",1,"prefix sum","Cumulative","algorithms.prefix-sum","algorithms.prefix-sum",
                _story("Dynamic Delta — Plains","Prefix Pioneer Pam","Build a running total so any range sum becomes one subtraction."),
                _tutor("Byte","🧭","prefix[i] = sum of elements before i. Then sum(i..j) = prefix[j+1] - prefix[i].","This turns repeated range sums into O(1) lookups."),
                _discover("Array [1,2,3,4]. Build prefix sums. Sum of indices 1 to 3?","prefix-build","Range sum","9"),
                _manipulate("cumulative","Build prefix[i] from prefix[i-1]","running total"),
                _predict("If prefix = [0,1,3,6,10], what is the sum of indices 1 to 2?","5","prefix[3] - prefix[1] = 6 - 1 = 5"),
                _break_step("What happens if you use prefix[j] - prefix[i] instead of prefix[j+1] - prefix[i]?","off-by-one: misses the last element","wrong range"),
                _debug("Fix the off-by-one: this returns 5 instead of 9 for indices 1..3.","arr=[1,2,3,4]\\ni,j=1,3\\nprefix=[0]\\nfor x in arr: prefix.append(prefix[-1]+x)\\nprint(prefix[j] - prefix[i])","Use j+1 because prefix includes the element at j.","arr=[1,2,3,4]\\ni,j=1,3\\nprefix=[0]\\nfor x in arr: prefix.append(prefix[-1]+x)\\nprint(prefix[j+1] - prefix[i])"),
                _code("Build prefix sums and answer one range-sum query.","nums = [1,2,3,4,5]\\n","prefix = [0]\\nfor x in nums:\\n    prefix.append(prefix[-1] + x)\\n# sum nums[1:4] = 2+3+4 = 9\\nprint(prefix[4] - prefix[1])"),
                _checks([r"prefix\\.append",r"prefix\\[-1\\]",r"prefix\\[j\\+1\\]\\s*-\\s*prefix\\[i\\]"]),
                ["Build cumulative sums.","Range sum is a subtraction.","prefix[0] = 0 for convenience."],
                _retrieval("What does prefix[i] represent?","sum of elements before index i","it is the cumulative total up to but not including i"),
                _transfer("Count the number of subarrays that sum to k using prefix sums.","nums=[1,2,3,4,5]\\nk=5\\nprefix=0\\ncount={0:1}\\nans=0\\nfor x in nums:\\n    prefix += x\\n    ans += count.get(prefix-k, 0)\\n    count[prefix] = count.get(prefix,0)+1\\nprint(ans)","same cumulative array, new query pattern"),
                _success("🧮 No prefix · ❌ Repeated summing","🧮 Prefix built · ✅ Range sums instant","Range queries are now O(1)!","Prefix Sum — cumulative magic.","Precompute once, query forever.",25)),
            _level("ps-2","The Difference Array","🛠️",2,"difference array","Range updates","algorithms.prefix-sum","algorithms.prefix-sum",
                _story("Dynamic Delta — Workshop","Difference Dara","Apply many range updates efficiently using a difference array."),
                _tutor("Byte","🧭","Instead of updating every element in a range, update only the boundaries and read the prefix at the end.","difference[start] += val, difference[end+1] -= val."),
                _discover("Range updates: add 3 to indices 1-3, add -2 to indices 2-4. Final array?","diff-apply","Final array","[0,3,1,1,-2,0]"),
                _manipulate("diff-boundary","Mark start and end+1 boundaries","difference array"),
                _predict("If you forget the end+1 correction, what goes wrong?","values after the range stay incorrect","tail remains wrong"),
                _break_step("What happens if you do difference[end] -= val instead of end+1?","only the end element is corrected, not the tail","partial fix"),
                _debug("Fix the partial update bug: indices after the range never recover.","diff=[0]*6\\ndiff[1]+=3\\ndiff[3]-=3\\n# missing end+1 for second update","Use end+1 so the prefix cancels the update after the range.","diff=[0]*6\\ndiff[1]+=3\\ndiff[4]-=3\\ndiff[2]+=-2\\ndiff[5]-=-2"),
                _code("Apply range updates using a difference array.","n = 6\\ndiff = [0] * (n + 1)\\nupdates = [(1,3,3),(2,4,-2)]\\n","for start, end, val in updates:\\n    diff[start] += val\\n    diff[end + 1] -= val\\nres = []\\ncur = 0\\nfor i in range(n):\\n    cur += diff[i]\\n    res.append(cur)\\nprint(res)"),
                _checks([r"diff\\[start\\]\\s*\\+=",r"diff\\[end\\s*\\+\\s*1\\]\\s*-=",r"for\\s+i\\s+in\\s+range"]),
                ["Update only the boundaries.","Prefix the difference array to get final values.","One pass for all updates."],
                _retrieval("Why is difference array better for many range updates?","O(1) per update instead of O(range length)","constant-time boundary edits"),
                _transfer("Use the same idea to schedule meeting room changes across a day.","hours=24\\ndiff=[0]*25\\nfor start,end,delta in meetings:\\n    diff[start]+=delta\\n    diff[end+1]-=delta\\ncur=0\\nfor h in range(24):\\n    cur+=diff[h]\\n    print(h, cur)","range-update pattern on time slots"),
                _success("🛠️ Range slow · ❌ Per-element updates","🛠️ Range batched · ✅ O(n+m)","All range updates are applied in one pass!","Difference Array — batch range updates.","Boundary edits + one prefix pass.",30)),
            _boss("ps-boss","The Subarray Sum","🎯",3,"prefix-master","Counting","algorithms.prefix-sum","algorithms.prefix-sum",
                _story("Dynamic Delta — Summit","Sum Sage","Count subarrays that sum to k using prefix sums and a hash map."),
                _tutor("Byte","🧭","If prefix[j] - prefix[i] = k, then subarray i..j-1 sums to k. Count matching pairs with a map.","prefix[j] seen before means there is an earlier subarray with the same sum."),
                _discover("Array [1,2,3,4,5], k=5. How many subarrays sum to 5?","count-subarrays","Count","3"),
                _manipulate("count-prefix","Track seen prefix sums in a map","hash map"),
                _predict("If prefix sum repeats, what does that mean?","the subarray between repeats sums to 0","zero-sum subarray"),
                _break_step("What happens if you forget to initialize seen with {0:1}?","you miss subarrays starting from index 0","off-by-one count"),
                _debug("Fix the missing-count bug: it returns 2 instead of 3.","count={}\\nprefix=0\\nans=0\\nfor x in nums:\\n    prefix += x\\n    ans += count.get(prefix-k,0)\\n    count[prefix] = count.get(prefix,0)+1\\nprint(ans)","Initialize count with {0:1} to include subarrays starting at index 0.","count={0:1}\\nprefix=0\\nans=0\\nfor x in nums:\\n    prefix += x\\n    ans += count.get(prefix-k,0)\\n    count[prefix] = count.get(prefix,0)+1\\nprint(ans)"),
                _code("Count subarrays that sum to k.","nums = [1,2,3,4,5]\\nk = 5\\n","count = {0: 1}\\nprefix = 0\\nans = 0\\nfor x in nums:\\n    prefix += x\\n    ans += count.get(prefix - k, 0)\\n    count[prefix] = count.get(prefix, 0) + 1\\nprint(ans)"),
                _checks([r"count\\[0\\]\\s*=\\s*1",r"prefix\\s*-=\\s*k",r"count\\.get\\("]),
                ["Track prefix sums in a map.","prefix[j] - prefix[i] = k means a valid subarray.","Initialize with {0:1}."],
                _retrieval("What does prefix sum repetition indicate?","a zero-sum subarray between repeats","same cumulative total twice"),
                _transfer("Find the maximum subarray sum using Kadane's algorithm, a cousin of prefix sums.","nums=[-2,1,-3,4,-1,2,1,-5,4]\\nbest=curr=nums[0]\\nfor x in nums[1:]:\\n    curr=max(x,curr+x)\\n    best=max(best,curr)\\nprint(best)","prefix-max pattern instead of counting"),
                _success("🎯 Subarrays missed · ❌ Under-count","🎯 Subarrays counted · ✅ Optimal","Every qualifying subarray is counted!","Prefix Sum Master — counting subarrays.","Cumulative sums + hash map = O(n).",45),
                _reward(diamonds=45,coins=25,badges=["prefix-master"],unlocks_town="town-2-graphs")),
        ]),
'''
    content = content.replace(marker, prefix_town + marker)
    
    with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('PREFIX TOWN INSERTED')
else:
    print('MARKER NOT FOUND')
