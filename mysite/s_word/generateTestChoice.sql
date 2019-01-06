-- 生成实词表并插入数据
CREATE TABLE "t_sword" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sword" varchar(4) NOT NULL);
create unique index t_sword_pk on t_sword('sword');
insert into t_sword(sword) select distinct sword from tmp_sword;

-- 生成实词含义表并插入数据
CREATE TABLE "t_swordmeaning" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                               "word_id" integer NOT NULL REFERENCES "t_sword" ("id"),
                               "pinyin" varchar(4) NOT NULL, 
                               "word_class" varchar(10) NOT NULL, 
                               "meaning" varchar(100) NOT NULL,
                               "difficulty" integer NOT NULL default 0);
create unique index t_swordmeaning_pk on t_swordmeaning(word_id,pinyin,word_class,meaning);
insert into t_swordmeaning(word_id,pinyin,word_class,meaning) 
select distinct b.id, a.pinyin, a. word_class, a.meaning
from tmp_sword a, t_sword b
where a.sword=b.sword;

-- 插入数据到例句表
insert into s_word_sword(sword, pinyin, word_class, meaning, sample, source, translation, swordmeaning_id)
select a.sword, a.pinyin, a.word_class, a.meaning, a.sample, a.source, a.translation, b.id
from tmp_sword a, t_swordmeaning b, t_sword c
where a.sword = c.sword
and   c.id = b.word_id
and   a.pinyin = b.pinyin
and   a.word_class = b.word_class
and   a.meaning = b.meaning
and   a.sample <> "";


-- 生成例句对应的题目
CREATE TABLE "t_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           "sword_id" integer NOT NULL REFERENCES "s_word_sword" ("id"),
                           "test_type" varchar(10) NOT NULL);
create unique index t_question_pk on t_question('sword_id','test_type');

-- 每个例句都有含义题
insert into t_question(sword_id,test_type) 
select distinct id, '含义' from s_word_sword;

-- 只有有拼音的才有拼音题
insert into t_question(sword_id,test_type) 
select distinct a.id, '拼音' 
from s_word_sword a,
     t_swordmeaning b
where a.swordmeaning_id=b.id
and   b.pinyin<>"";

-- 只有词性多于1个的才有词性题
insert into t_question(sword_id,test_type) 
select c.id, '词性'
from
    (select word_id,count(distinct word_class) from t_swordmeaning group by word_id having count(distinct word_class)>1) a,
    t_swordmeaning b,
    s_word_sword c
where a.word_id=b.word_id
and  b.id=c.swordmeaning_id;


-- 生成题目选项：含义
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct, question_id_id) 
select distinct a.sword_id, a.test_type, 
       d.meaning||'【'||d.word_class||'】', 
       (case when d.meaning=c.meaning and d.word_class=c.word_class then 1 else 0 end) is_correct,
       a.id
from t_question a,
     s_word_sword b,
     t_swordmeaning c,
     t_swordmeaning d
where a.sword_id=b.id
and   b.swordmeaning_id =c.id
and   c.word_id=d.word_id
and   a.test_type='含义';

-- 生成题目选项：拼音
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct, question_id_id) 
select distinct a.sword_id, a.test_type, d.pinyin, 
       (case when d.pinyin=c.pinyin then 1 else 0 end) is_correct,
       a.id
from t_question a,
     s_word_sword b,
     t_swordmeaning c,
     t_swordmeaning d
where a.sword_id=b.id
and   b.swordmeaning_id =c.id
and   c.word_id=d.word_id
and   a.test_type='拼音';

-- 生成题目选项：词性
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct, question_id_id) 
select distinct a.sword_id, a.test_type, d.word_class, 
       (case when d.word_class=c.word_class then 1 else 0 end) is_correct,
       a.id
from t_question a,
     s_word_sword b,
     t_swordmeaning c,
     t_swordmeaning d
where a.sword_id=b.id
and   b.swordmeaning_id =c.id
and   c.word_id=d.word_id
and   a.test_type='词性';


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
select c.id, a.sword_id, sword, a.test_type, user_id, max(test_date) pass_date
from s_word_swordtest a,
     s_word_sword b,
     t_question c
where a.test_result=1
and a.sword_id=b.id
and a.sword_id=c.sword_id
and a.test_type=c.test_type
group by a.sword_id, sword, a.test_type, user_id;

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

-- 用户每个实词的测试通过情况（没有记录以及有记录但没有100分的记录的且当天没有测试记录）