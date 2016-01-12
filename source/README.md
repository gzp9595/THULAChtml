# THULAC：一个高效的中文词法分析工具包
##目录
* [项目介绍](#项目介绍)
* [编译和安装](#编译和安装)
* [使用](#使用)
* [代表分词软件的性能对比](#代表分词软件的性能对比)
* [词性解释](#词性解释)
* [THULAC模型介绍](#THULAC模型介绍)
* [获取链接](#获取链接)
* [注意事项](#注意事项)
* [开源协议](#开源协议)
* [相关论文](#相关论文)
* [作者](#作者)

##项目介绍

THULAC（THU Lexical Analyzer for Chinese）是由清华大学自然语言处理实验室推出的一套中文词法分析工具包，主要包括中文分词和词性标注功能。THULAC具有如下几个特点：

1. 算法新颖。该工具包使用了基于词图（word lattice）的重排序算法（re-ranking method），在分词、词性标注和重排序方面效率较高，性能较强。

2. 模型强大。我们按照统一标注规范整合多个分词、词性标注语料库，得到一份1500万字的分词、词性标注语料库（大小约300M）用于模型训练，模型标注能力强大。

3. 准确率高。该工具包在标准数据集Chinese Treebank（CTB5）上分词的F1值可达97.3％，词性标注的F1值可达到92.9％，与该数据集上最好方法效果相当。

4. 速度较快。该工具包的分词和词性标注速度为300KB/s，每秒可处理约15万字。仅进行分词速度可达到1.3MB/s。

##编译和安装
	在当前路径下运行
	make
	会在当前目录下得到thulac和train_c

##使用
####命令格式为：

* ./thulac [-t2s] [-seg_only] [-deli delimeter] [-user userword.txt]   从命令行输入输出
* ./thulac [-t2s] [-seg_only] [-deli delimeter] [-user userword.txt] <inputfile >outputfile   利用重定向从文本文件输入输出（注意均为UTF8文本）

####参数意义:
	-t2s			    将句子从繁体转化为简体
	-seg_only		    只进行分词，不进行词性标注
	-deli delimeter		设置词与词性间的分隔符，默认为下划线_
	-user userword.txt	设置用户词典，用户词典中的词会被打上uw标签。词典中每一个词一行，UTF8编码
	-model_dir dir		设置模型文件所在文件夹，默认为models/


##代表分词软件的性能对比
我们选择LTP、ICTCLAS、结巴分词等国内代表分词软件与THULAC做性能比较。我们选择Windows作为测试环境，根据第二届国际汉语分词测评发布的国际中文分词测评标准，对不同软件进行了速度和准确率测试。

在第二届国际汉语分词测评中，共有四家单位提供的测试语料（Academia Sinica、 City University 、Peking University 、Microsoft Research）, 在评测提供的资源[icwb2-data](http://www.sighan.org/bakeoff2005/)中包含了来自这四家单位的训练集（training）、测试集（testing）, 以及根据各自分词标准而提供的相应测试集的标准答案（icwb2-data/scripts/gold）．在icwb2-data/scripts目录下含有对分词进行自动评分的perl脚本score。

我们在统一测试环境下，对若干流行分词软件和THULAC进行了测试，使用的模型为各分词软件自带模型。THULAC使用的是随软件提供的简单模型Model_1。评测环境为 Intel Core i5 2.4 GHz 评测结果如下：

msr_test（560KB）

Algorithm | Time| Precision | Recall
:------------ | ------------- :| ------------ :| -------:
LTP-3.2.0 | 3.21s  | 0.867 | 0.896
ICTCLAS(2015版) | 0.55s | 0.869 | 0.914
jieba(C++版)|0.26s|0.814|0.809
THULAC | 0.62s  | 0.877 | 0.899

pku_test（510KB）

Algorithm | Time| Precision | Recall
:------------ | ------------- :| ------------: | -------:
LTP-3.2.0 | 3.83s  | 0.960 | 0.947
ICTCLAS(2015版) | 0.53s | 0.939 | 0.944
jieba(C++版)|0.23s|0.850|0.784
THULAC | 0.51s  | 0.944 | 0.908

除了以上在标准测试集上的评测，我们也对各个分词工具在大数据上的速度进行了评测，结果如下：

CNKI_journal.txt（51 MB）

Algorithm | Time | Speed
:------------ | ------------- :| ------------:
LTP-3.2.0 | 348.624s  | 149.80KB/s
ICTCLAS(2015版) | 106.461s | 490.59KB/s
jieba(C++版)|22.5583s|2314.89KB/s
THULAC | 42.625s  | 1221.05KB/s

##词性解释
	a/形容词 c/连词 d/副词 e/语气词 f/方位词 g/助词
    h/前接成分 id/习语 j/简称 k/后接成分 l/处所词
    m/数词 mq/数量词 n/名词 ni/机构名 np/人名
    ns/地名 nz/其它专名 o/拟声词 p/介词 q/量词
    r/代词 t/时间词 u/助词 v/动词 w/标点 x/其它

##THULAC模型介绍
1. 我们随THULAC源代码附带了简单的分词模型Model_1，仅支持分词功能。该模型由北京大学人民日报分词语料库训练得到（数据大小约56M，原始分词语料请联系北京大学计算语言学研究所授权获取）。

2. 我们随THULAC源代码附带了分词和词性标注联合模型Model_2，支持同时分词和词性标注功能。该模型由多个分词语料库训练数据联合训练得到（大小约300M）。

3. 我们还提供更复杂、完善和精确的分词和词性标注联合模型Model_3和分词词表。由于模型较大，如有机构或个人需要，请填写“doc/资源申请表.doc”，并发送至 thunlp@gmail.com ，通过审核后我们会将相关资源发送给联系人。


##获取链接

Source | Description | Size|Data
:------------ | :------------- | ------------:|--------:
THULAC_c++_v1.tar.gz| THULAC分词源代码 | 46KB|2016-01-11
Models_1_2.zip | THULAC模型，包括分词模型以及分词和词性标注联合模型 | 53.1MB|2016-01-11
Models_3.zip|THULAC模型，包括更复杂完善的分词和词性标注模型以及分词词表|162.7MB|2016-01-11

##注意事项

该工具目前仅处理UTF8编码中文文本，之后会逐渐增加支持其他编码的功能，敬请期待。


##开源协议
1. THULAC面向国内外大学、研究所、企业以及个人研究者免费开放源。
2. 如有机构或个人拟将THULAC用于商业目的，请发邮件至thunlp@gmail.com洽谈技术许可协议。
3. 欢迎对该工具包的任何宝贵意见和建议，请发邮件至thunlp@gmail.com。
4. 如果您在THULAC基础上发表论文或取得科研成果，请您在发表论文和申报成果时声明“使用了清华大学THULAC”，并按如下格式引用：
	
	* **中文： 孙茂松, 陈新雄, 郭志芃, 张开旭, 刘知远. THULAC：一个高效的中文词法分析工具包. 2016.**
	
	* **英文： Maosong Sun, Xinxiong Chen, Zhipeng Guo, Kaixu Zhang, Zhiyuan Liu. THULAC: An Efficient Lexical Analyzer for Chinese. 2016.**
		
   同时，发信给thunlp@gmail.com，说明发表论文或申报成果的题目、出处等。
   
##相关论文
* Zhongguo Li, Maosong Sun. Punctuation as Implicit Annotations for Chinese Word Segmentation. Computational Linguistics, vol. 35, no. 4, pp. 505-512, 2009.
   
##作者

指导教师：Maosong Sun （孙茂松教授）

贡献者：Xinxiong Chen（陈新雄）, Zhipeng Guo（郭志芃）, Kaixu Zhang (张开旭), Zhiyuan Liu（刘知远）.

使用者如有任何问题、建议和意见，欢迎发邮件至 thunlp@gmail.com 。
