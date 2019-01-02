-- generate pinyin test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'拼音', b.pinyin, a.pinyin=b.pinyin 
    from s_word_sword a, 
        (select distinct sword, pinyin from s_word_sword where pinyin<>"" ) b,
        (select sword from s_word_sword where pinyin<>"" group by sword having count(distinct pinyin)>1) c
    where a.sword=b.sword
    and b.sword=c.sword
    and a.sample<>"";
-- generate word_class test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'词性', b.word_class, a.word_class=b.word_class 
    from s_word_sword a, 
        (select distinct sword, word_class from s_word_sword) b,
        (select sword from s_word_sword group by sword having count(distinct word_class)>1) c
    where a.sword=b.sword
    and b.sword=c.sword
    and a.sample<>"";
-- generate meaning test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'含义', b.meaning||'【'||b.word_class||'】', b.meaning||'【'||b.word_class||'】'=a.meaning||'【'||a.word_class||'】'
    from s_word_sword a, 
        (select distinct sword, meaning, word_class from s_word_sword ) b 
    where a.sword=b.sword
    and a.sample<>"";

-- create word table to provide id
CREATE TABLE "t_sword" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sword" varchar(4) NOT NULL);
insert into t_sword(sword) select distinct sword from s_word_sword;

-- create question table to provide id
CREATE TABLE "t_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           "sword_id" integer NOT NULL REFERENCES "s_word_sword" ("id"),
                           "test_type" varchar(10) NOT NULL);
insert into t_question(sword_id,test_type) select distinct sword_id, test_type from s_word_swordtest1choice;
ß
-- create view 
-- view of question list
create view v_swordtestquestion as
select b.*, a.sword,a.sample from s_word_sword a, (select distinct sword_id, test_type from s_word_swordtest1choice) b where a.id=b.sword_id;

-- view of how many questions relate to one word
create view v_swordtestquestion_count as 
select t2.id, t1.sword, count(*) questioncount 
from v_swordtestquestion t1, t_sword t2 
where t1.sword=t2.sword
group by t1.sword
order by t2.id;

-- view of how many questions relate to one word by test_type
create view v_swordtestquestion_count_bytype as 
select sword, test_type, count(*) questioncount from v_swordtestquestion group by sword, test_type;

-- view for user passed question list 
create view v_user_passed_question as
select sword_id, sword, test_type, user_id, max(test_date) pass_date
from s_word_swordtest a,
     s_word_sword b
where a.test_result=1
and a.sword_id=b.id
group by sword_id, sword, test_type, user_id;

-- view user's how many passed question by word
create view v_user_passed_question_count as
select c.id, a.sword, a.user_id,count(*) passedcount, b.questioncount, 
       (case when count(*) = b.questioncount then "passed" else "inprogress" end) status
from v_user_passed_question a,
     v_swordtestquestion_count b,
     t_sword c
where a.sword=b.sword
and b.sword=c.sword
group by a.sword, a.user_id
order by c.id ;

-- view user's how many passed question by word
create view v_user_passed_question_count_bytype as
select a.sword, a.user_id, a.test_type, count(*) passedcount, b.questioncount, 
       (case when count(*) = b.questioncount then "passed" else "inprogress" end) status
from v_user_passed_question a,
     v_swordtestquestion_count_bytype b
where a.sword=b.sword
and a.test_type=b.test_type
group by a.sword, a.user_id, a.test_type;

-- 最后一次答题情况视图
create view v_user_latest_testresult_by_question as
select b.*
from 
    (select sword_id, user_id, test_type, max(test_date) test_date
    from s_word_swordtest
    group by sword_id, user_id, test_type) a,  
    s_word_swordtest b
where a.sword_id=b.sword_id
and   a.user_id=b.user_id
and   a.test_type=b.test_type
and   a.test_date=b.test_date;

-- 错误分值-0.6，正确的0.4，给同一试题所有得分相加，以及加上最近一次答题是错误的题目（扣1分）。 总分值<0的题需要重新复习。
create view v_user_question_score as 
select c.id, a.sword_id, a.user_id, a.test_type, (score + b.test_result - 1 ) score
from
    (select sword_id, user_id, test_type, sum((test_result-0.6)) score
    from s_word_swordtest
    group by sword_id, user_id, test_type) a,
    v_user_latest_testresult_by_question b,
    t_question c
where a.sword_id=b.sword_id
and   a.user_id=b.user_id
and   a.test_type=b.test_type
and  a.sword_id=c.sword_id
and  a.test_type=c.test_type
order by score;
