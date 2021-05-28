html(
_lang="en", _op="news",
head(
meta(
_name="referrer", _content="origin",
),
meta(
_name="viewport", _content="width=device-width, initial-scale=1.0",
),
link(
_rel="stylesheet", _type="text/css", _href="news.css?wRBQvoWTalI3lUyNpVaE",
),
link(
_rel="shortcut icon", _href="favicon.ico",
),
link(
_rel="alternate", _type="application/rss+xml", _title="RSS", _href="rss",
),
title(
"Hacker News"
),
),
body(
center(
table(
_id="hnmain", _border="0", _cellpadding="0", _cellspacing="0", _width="85%", _bgcolor="#f6f6ef",
tr(
td(
_bgcolor="#ff6600",
table(
_border="0", _cellpadding="0", _cellspacing="0", _width="100%", _style="padding:2px",
tr(
td(
_style="width:18px;padding-right:4px",
a(
_href="https://news.ycombinator.com",
img(
_src="y18.gif", _width="18", _height="18", _style="border:1px white solid;",
),
),
td(
_style="line-height:12pt; height:10px;",
span(
_class="pagetop",
b(
_class="hnname",
a(
_href="news",
"Hacker News"
),
),
a(
_href="newest",
"new"
),
"|",
a(
_href="front",
"past"
),
"|",
a(
_href="newcomments",
"comments"
),
"|",
a(
_href="ask",
"ask"
),
"|",
a(
_href="show",
"show"
),
"|",
a(
_href="jobs",
"jobs"
),
"|",
a(
_href="submit",
"submit"
),
),
),
td(
_style="text-align:right;padding-right:4px;",
span(
_class="pagetop",
a(
_href="login?goto=news",
"login"
),
),
),
),
),
),
),
tr(
_id="pagespace", _title="", _style="height:10px",
),
tr(
td(
table(
_border="0", _cellpadding="0", _cellspacing="0", _class="itemlist",
tr(
_class='athing' ,   _id='27300799',
td(
span(
_class="rank",
"1."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300799' ,   _href='vote?, _id=27300799&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.reuters.com/world/europe/protasevich-street-bucharest-mulls-changing-address-belarusian-embassy-2021-05-27/", _class="storylink",
"Protasevich Street? Bucharest mulls changing address of Belarusian embassy"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=reuters.com",
span(
_class="sitestr",
"reuters.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300799",
"73 points"
),
"by",
a(
_href="user?id=johnnycerberus", _class="hnuser",
"johnnycerberus"
),
span(
_class="age",
a(
_href="item?id=27300799",
"1 hour ago"
),
),
span(
_id="unv_27300799",
),
"|",
a(
_href="hide?id=27300799&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300799",
"27&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300843',
td(
span(
_class="rank",
"2."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300843' ,   _href='vote?, _id=27300843&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.bbc.com/news/technology-57254488", _class="storylink",
"Instagram lets users hide likes to reduce social media pressure"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=bbc.com",
span(
_class="sitestr",
"bbc.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300843",
"13 points"
),
"by",
a(
_href="user?id=shivbhatt", _class="hnuser",
"shivbhatt"
),
span(
_class="age",
a(
_href="item?id=27300843",
"56 minutes ago"
),
),
span(
_id="unv_27300843",
),
"|",
a(
_href="hide?id=27300843&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300843",
"1&nbsp;comment"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27295906',
td(
span(
_class="rank",
"3."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27295906' ,   _href='vote?, _id=27295906&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://m-cacm.acm.org/magazines/2021/6/252840-collusion-rings-threaten-the-integrity-of-computer-science-research/fulltext", _class="storylink",
"Collusion rings threaten the integrity of computer science research"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=acm.org",
span(
_class="sitestr",
"acm.org"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27295906",
"581 points"
),
"by",
a(
_href="user?id=djoldman", _class="hnuser",
"djoldman"
),
span(
_class="age",
a(
_href="item?id=27295906",
"13 hours ago"
),
),
span(
_id="unv_27295906",
),
"|",
a(
_href="hide?id=27295906&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27295906",
"308&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27297689',
td(
span(
_class="rank",
"4."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27297689' ,   _href='vote?, _id=27297689&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://river-runner.samlearner.com/", _class="storylink",
"River Runner: drop a raindrop anywhere in the USA, watch where it ends up"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=samlearner.com",
span(
_class="sitestr",
"samlearner.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27297689",
"340 points"
),
"by",
a(
_href="user?id=prawn", _class="hnuser",
"prawn"
),
span(
_class="age",
a(
_href="item?id=27297689",
"10 hours ago"
),
),
span(
_id="unv_27297689",
),
"|",
a(
_href="hide?id=27297689&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27297689",
"44&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27287644',
td(
span(
_class="rank",
"5."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27287644' ,   _href='vote?, _id=27287644&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://github.com/b4rtaz/voice-assistant", _class="storylink",
"Programming by Voice for Visual Studio Code"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=github.com/b4rtaz",
span(
_class="sitestr",
"github.com/b4rtaz"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27287644",
"21 points"
),
"by",
a(
_href="user?id=b4rtaz__", _class="hnuser",
"b4rtaz__"
),
span(
_class="age",
a(
_href="item?id=27287644",
"1 hour ago"
),
),
span(
_id="unv_27287644",
),
"|",
a(
_href="hide?id=27287644&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27287644",
"4&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300833',
td(
span(
_class="rank",
"6."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300833' ,   _href='vote?, _id=27300833&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.bbc.com/news/business-57254962", _class="storylink",
"Uber recognises union for first time in landmark deal"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=bbc.com",
span(
_class="sitestr",
"bbc.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300833",
"9 points"
),
"by",
a(
_href="user?id=shivbhatt", _class="hnuser",
"shivbhatt"
),
span(
_class="age",
a(
_href="item?id=27300833",
"56 minutes ago"
),
),
span(
_id="unv_27300833",
),
"|",
a(
_href="hide?id=27300833&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300833",
"discuss"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27292219',
td(
span(
_class="rank",
"7."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27292219' ,   _href='vote?, _id=27292219&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://blog.nikitas.link/have-you-ever-hurt-yourself-from-your-own-code", _class="storylink",
"Have you ever hurt yourself from your own code?"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=nikitas.link",
span(
_class="sitestr",
"nikitas.link"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27292219",
"328 points"
),
"by",
a(
_href="user?id=its_nikita", _class="hnuser",
"its_nikita"
),
span(
_class="age",
a(
_href="item?id=27292219",
"11 hours ago"
),
),
span(
_id="unv_27292219",
),
"|",
a(
_href="hide?id=27292219&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27292219",
"180&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27298422',
td(
span(
_class="rank",
"8."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27298422' ,   _href='vote?, _id=27298422&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://github.com/OpenHD/Open.HD", _class="storylink",
"OpenHD - HD video, UAV telemetry, audio, and RC control"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=github.com/openhd",
span(
_class="sitestr",
"github.com/openhd"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27298422",
"140 points"
),
"by",
a(
_href="user?id=danboarder", _class="hnuser",
"danboarder"
),
span(
_class="age",
a(
_href="item?id=27298422",
"8 hours ago"
),
),
span(
_id="unv_27298422",
),
"|",
a(
_href="hide?id=27298422&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27298422",
"22&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27283521',
td(
span(
_class="rank",
"9."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27283521' ,   _href='vote?, _id=27283521&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://squidfunk.github.io/mkdocs-material/", _class="storylink",
"Technical documentation that just works"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=squidfunk.github.io",
span(
_class="sitestr",
"squidfunk.github.io"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27283521",
"102 points"
),
"by",
a(
_href="user?id=dedalus", _class="hnuser",
"dedalus"
),
span(
_class="age",
a(
_href="item?id=27283521",
"6 hours ago"
),
),
span(
_id="unv_27283521",
),
"|",
a(
_href="hide?id=27283521&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27283521",
"43&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27294890',
td(
span(
_class="rank",
"10."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27294890' ,   _href='vote?, _id=27294890&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://github.blog/2021-05-26-why-and-how-github-is-adopting-opentelemetry/", _class="storylink",
"Why and how GitHub is adopting OpenTelemetry"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=github.blog",
span(
_class="sitestr",
"github.blog"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27294890",
"312 points"
),
"by",
a(
_href="user?id=todsacerdoti", _class="hnuser",
"todsacerdoti"
),
span(
_class="age",
a(
_href="item?id=27294890",
"14 hours ago"
),
),
span(
_id="unv_27294890",
),
"|",
a(
_href="hide?id=27294890&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27294890",
"83&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300206',
td(
span(
_class="rank",
"11."
),
),
td(
),
td(
_class="title",
a(
_href="https://www.workatastartup.com/jobs/43955", _class="storylink", _rel="nofollow",
"Promoted.ai (YC W21) Is Hiring SRE/DevOps"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=workatastartup.com",
span(
_class="sitestr",
"workatastartup.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="age",
a(
_href="item?id=27300206",
"3 hours ago"
),
),
"|",
a(
_href="hide?id=27300206&amp;goto=news",
"hide"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27298862',
td(
span(
_class="rank",
"12."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27298862' ,   _href='vote?, _id=27298862&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.well.com/", _class="storylink",
"Whole Earth ‘Lectronic Link"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=well.com",
span(
_class="sitestr",
"well.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27298862",
"50 points"
),
"by",
a(
_href="user?id=graderjs", _class="hnuser",
"graderjs"
),
span(
_class="age",
a(
_href="item?id=27298862",
"7 hours ago"
),
),
span(
_id="unv_27298862",
),
"|",
a(
_href="hide?id=27298862&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27298862",
"32&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300414',
td(
span(
_class="rank",
"13."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300414' ,   _href='vote?, _id=27300414&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.llnl.gov/news/satellites-may-have-underestimated-warming-lower-atmosphere", _class="storylink", _rel="nofollow",
"Satellites may have underestimated warming in the lower atmosphere"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=llnl.gov",
span(
_class="sitestr",
"llnl.gov"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300414",
"6 points"
),
"by",
a(
_href="user?id=ulnarkressty", _class="hnuser",
"ulnarkressty"
),
span(
_class="age",
a(
_href="item?id=27300414",
"2 hours ago"
),
),
span(
_id="unv_27300414",
),
"|",
a(
_href="hide?id=27300414&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300414",
"discuss"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27287987',
td(
span(
_class="rank",
"14."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27287987' ,   _href='vote?, _id=27287987&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://kean.blog/post/lets-build-regex", _class="storylink",
"Let's Build a Regex Engine"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=kean.blog",
span(
_class="sitestr",
"kean.blog"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27287987",
"122 points"
),
"by",
a(
_href="user?id=asicsp", _class="hnuser",
"asicsp"
),
span(
_class="age",
a(
_href="item?id=27287987",
"11 hours ago"
),
),
span(
_id="unv_27287987",
),
"|",
a(
_href="hide?id=27287987&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27287987",
"26&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27289213',
td(
span(
_class="rank",
"15."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27289213' ,   _href='vote?, _id=27289213&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://spectrum.ieee.org/geek-life/hands-on/build-a-riscv-cpu-from-scratch", _class="storylink",
"Build a RISC-V CPU from scratch"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=ieee.org",
span(
_class="sitestr",
"ieee.org"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27289213",
"87 points"
),
"by",
a(
_href="user?id=azhenley", _class="hnuser",
"azhenley"
),
span(
_class="age",
a(
_href="item?id=27289213",
"10 hours ago"
),
),
span(
_id="unv_27289213",
),
"|",
a(
_href="hide?id=27289213&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27289213",
"21&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300594',
td(
span(
_class="rank",
"16."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300594' ,   _href='vote?, _id=27300594&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="item?id=27300594", _class="storylink",
"Ask HN: Anybody Started a Research Institute?"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300594",
"8 points"
),
"by",
a(
_href="user?id=akhann", _class="hnuser",
"akhann"
),
span(
_class="age",
a(
_href="item?id=27300594",
"1 hour ago"
),
),
span(
_id="unv_27300594",
),
"|",
a(
_href="hide?id=27300594&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300594",
"2&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27281714',
td(
span(
_class="rank",
"17."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27281714' ,   _href='vote?, _id=27281714&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.nytimes.com/2021/05/24/books/review-languages-of-truth-salman-rushdie-essays.html", _class="storylink",
"In ‘Languages of Truth,’ Salman Rushdie Defends the Extraordinary"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=nytimes.com",
span(
_class="sitestr",
"nytimes.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27281714",
"9 points"
),
"by",
a(
_href="user?id=lermontov", _class="hnuser",
"lermontov"
),
span(
_class="age",
a(
_href="item?id=27281714",
"4 hours ago"
),
),
span(
_id="unv_27281714",
),
"|",
a(
_href="hide?id=27281714&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27281714",
"discuss"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27300548',
td(
span(
_class="rank",
"18."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27300548' ,   _href='vote?, _id=27300548&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.topic.com/the-penis-poster-that-rubbed-people-the-wrong-way", _class="storylink", _rel="nofollow",
"The poster that rubbed people the wrong way"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=topic.com",
span(
_class="sitestr",
"topic.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27300548",
"4 points"
),
"by",
a(
_href="user?id=wombatmobile", _class="hnuser",
"wombatmobile"
),
span(
_class="age",
a(
_href="item?id=27300548",
"1 hour ago"
),
),
span(
_id="unv_27300548",
),
"|",
a(
_href="hide?id=27300548&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27300548",
"1&nbsp;comment"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27287938',
td(
span(
_class="rank",
"19."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27287938' ,   _href='vote?, _id=27287938&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.atlasobscura.com/articles/paris-subway-station-movie-location", _class="storylink",
"Ghost subway station in Paris where films come to life"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=atlasobscura.com",
span(
_class="sitestr",
"atlasobscura.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27287938",
"67 points"
),
"by",
a(
_href="user?id=CaptainZapp", _class="hnuser",
"CaptainZapp"
),
span(
_class="age",
a(
_href="item?id=27287938",
"8 hours ago"
),
),
span(
_id="unv_27287938",
),
"|",
a(
_href="hide?id=27287938&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27287938",
"8&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27282814',
td(
span(
_class="rank",
"20."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27282814' ,   _href='vote?, _id=27282814&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://github.com/robert-strandh/SICL", _class="storylink",
"SICL: A New Common Lisp Implementation"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=github.com/robert-strandh",
span(
_class="sitestr",
"github.com/robert-strandh"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27282814",
"120 points"
),
"by",
a(
_href="user?id=tosh", _class="hnuser",
"tosh"
),
span(
_class="age",
a(
_href="item?id=27282814",
"14 hours ago"
),
),
span(
_id="unv_27282814",
),
"|",
a(
_href="hide?id=27282814&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27282814",
"35&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27291302',
td(
span(
_class="rank",
"21."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27291302' ,   _href='vote?, _id=27291302&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://crispgm.com/page/neovim-is-overpowering.html", _class="storylink",
"Neovim 0.5 is overpowering"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=crispgm.com",
span(
_class="sitestr",
"crispgm.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27291302",
"689 points"
),
"by",
a(
_href="user?id=imbnwa", _class="hnuser",
"imbnwa"
),
span(
_class="age",
a(
_href="item?id=27291302",
"19 hours ago"
),
),
span(
_id="unv_27291302",
),
"|",
a(
_href="hide?id=27291302&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27291302",
"377&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27298343',
td(
span(
_class="rank",
"22."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27298343' ,   _href='vote?, _id=27298343&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://onezero.medium.com/a-i-is-solving-the-wrong-problem-253b636770cd", _class="storylink",
"A.I. Is Solving the Wrong Problem"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=onezero.medium.com",
span(
_class="sitestr",
"onezero.medium.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27298343",
"49 points"
),
"by",
a(
_href="user?id=mbellotti", _class="hnuser",
"mbellotti"
),
span(
_class="age",
a(
_href="item?id=27298343",
"8 hours ago"
),
),
span(
_id="unv_27298343",
),
"|",
a(
_href="hide?id=27298343&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27298343",
"36&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27284898',
td(
span(
_class="rank",
"23."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27284898' ,   _href='vote?, _id=27284898&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.hakaimagazine.com/features/that-time-hitlers-girlfriend-visited-iceland-and-the-british-invaded/", _class="storylink",
"Iceland played an unexpected and crucial role in the Second World War"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=hakaimagazine.com",
span(
_class="sitestr",
"hakaimagazine.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27284898",
"46 points"
),
"by",
a(
_href="user?id=Thevet", _class="hnuser",
"Thevet"
),
span(
_class="age",
a(
_href="item?id=27284898",
"10 hours ago"
),
),
span(
_id="unv_27284898",
),
"|",
a(
_href="hide?id=27284898&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27284898",
"11&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27299839',
td(
span(
_class="rank",
"24."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27299839' ,   _href='vote?, _id=27299839&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://rachelbythebay.com/w/2021/05/26/irc/", _class="storylink",
"IRC: Run it or use it, but try to avoid doing both"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=rachelbythebay.com",
span(
_class="sitestr",
"rachelbythebay.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27299839",
"47 points"
),
"by",
a(
_href="user?id=Tomte", _class="hnuser",
"Tomte"
),
span(
_class="age",
a(
_href="item?id=27299839",
"4 hours ago"
),
),
span(
_id="unv_27299839",
),
"|",
a(
_href="hide?id=27299839&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27299839",
"7&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27293902',
td(
span(
_class="rank",
"25."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27293902' ,   _href='vote?, _id=27293902&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.findareddit.com/", _class="storylink",
"Show HN: Find Subreddits for Your Niche"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=findareddit.com",
span(
_class="sitestr",
"findareddit.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27293902",
"344 points"
),
"by",
a(
_href="user?id=thisissidhant", _class="hnuser",
"thisissidhant"
),
span(
_class="age",
a(
_href="item?id=27293902",
"16 hours ago"
),
),
span(
_id="unv_27293902",
),
"|",
a(
_href="hide?id=27293902&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27293902",
"162&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27289479',
td(
span(
_class="rank",
"26."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27289479' ,   _href='vote?, _id=27289479&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.smithsonianmag.com/science-nature/why-ecologists-are-haunted-rapid-growth-ghost-forests-180977674/", _class="storylink",
"A study in North Carolina of dying trees"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=smithsonianmag.com",
span(
_class="sitestr",
"smithsonianmag.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27289479",
"62 points"
),
"by",
a(
_href="user?id=ryan_j_naughton", _class="hnuser",
"ryan_j_naughton"
),
span(
_class="age",
a(
_href="item?id=27289479",
"7 hours ago"
),
),
span(
_id="unv_27289479",
),
"|",
a(
_href="hide?id=27289479&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27289479",
"29&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27286670',
td(
span(
_class="rank",
"27."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27286670' ,   _href='vote?, _id=27286670&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="http://thepassingtramp.blogspot.com/2012/05/faulkner-vs-wellman-ellery-queens.html", _class="storylink", _rel="nofollow",
"Faulkner vs. Wellman: The Ellery Queen's Mystery Magazine 1946 Showdown (2012)"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=thepassingtramp.blogspot.com",
span(
_class="sitestr",
"thepassingtramp.blogspot.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27286670",
"5 points"
),
"by",
a(
_href="user?id=samclemens", _class="hnuser",
"samclemens"
),
span(
_class="age",
a(
_href="item?id=27286670",
"3 hours ago"
),
),
span(
_id="unv_27286670",
),
"|",
a(
_href="hide?id=27286670&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27286670",
"discuss"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27288394',
td(
span(
_class="rank",
"28."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27288394' ,   _href='vote?, _id=27288394&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.sciencealert.com/enigmatic-designs-found-in-india-may-be-the-largest-images-ever-made-by-human-hands", _class="storylink",
"Enigmatic designs found in India may be the largest images made by human hands"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=sciencealert.com",
span(
_class="sitestr",
"sciencealert.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27288394",
"83 points"
),
"by",
a(
_href="user?id=samizdis", _class="hnuser",
"samizdis"
),
span(
_class="age",
a(
_href="item?id=27288394",
"15 hours ago"
),
),
span(
_id="unv_27288394",
),
"|",
a(
_href="hide?id=27288394&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27288394",
"18&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27283328',
td(
span(
_class="rank",
"29."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27283328' ,   _href='vote?, _id=27283328&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://www.theguardian.com/books/2021/may/24/architecture-from-prehistory-to-climate-emergency-barnabas-calder-review", _class="storylink",
"Architecture: From Prehistory to Climate Emergency Review"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=theguardian.com",
span(
_class="sitestr",
"theguardian.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27283328",
"10 points"
),
"by",
a(
_href="user?id=tintinnabula", _class="hnuser",
"tintinnabula"
),
span(
_class="age",
a(
_href="item?id=27283328",
"5 hours ago"
),
),
span(
_id="unv_27283328",
),
"|",
a(
_href="hide?id=27283328&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27283328",
"1&nbsp;comment"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class='athing' ,   _id='27293108',
td(
span(
_class="rank",
"30."
),
),
td(
_valign="top", _class="votelinks",
center(
a(
_id='up_27293108' ,   _href='vote?, _id=27293108&amp;how=up&amp;goto=news',
div(
_class='votearrow' ,   _title='upvote',
),
),
),
),
td(
_class="title",
a(
_href="https://rubenerd.com/using-netbsds-pkgsrc-everywhere-i-can/", _class="storylink",
"Using NetBSD’s pkgsrc everywhere I can"
),
span(
_class="sitebit comhead",
"(",
a(
_href="from?site=rubenerd.com",
span(
_class="sitestr",
"rubenerd.com"
),
),
")"
),
),
),
tr(
td(
_colspan="2",
),
td(
_class="subtext",
span(
_class="score", _id="score_27293108",
"94 points"
),
"by",
a(
_href="user?id=jayp1418", _class="hnuser",
"jayp1418"
),
span(
_class="age",
a(
_href="item?id=27293108",
"17 hours ago"
),
),
span(
_id="unv_27293108",
),
"|",
a(
_href="hide?id=27293108&amp;goto=news",
"hide"
),
"|",
a(
_href="item?id=27293108",
"56&nbsp;comments"
),
),
),
tr(
_class="spacer", _style="height:5px",
),
tr(
_class="morespace", _style="height:10px",
),
tr(
td(
_colspan="2",
),
td(
_class="title",
a(
_href="news?p=2", _class="morelink", _rel="next",
"More"
),
),
),
),
),
),
tr(
td(
img(
_src="s.gif", _height="10", _width="0",
table(
_width="100%", _cellspacing="0", _cellpadding="1",
tr(
td(
_bgcolor="#ff6600",
),
),
),
br(
center(
span(
_class="yclinks",
a(
_href="newsguidelines.html",
"Guidelines"
),
"|",
a(
_href="newsfaq.html",
"FAQ"
),
"|",
a(
_href="lists",
"Lists"
),
"|",
a(
_href="https://github.com/HackerNews/API",
"API"
),
"|",
a(
_href="security.html",
"Security"
),
"|",
a(
_href="http://www.ycombinator.com/legal/",
"Legal"
),
"|",
a(
_href="http://www.ycombinator.com/apply/",
"Apply to YC"
),
"|",
a(
_href="mailto:hn@ycombinator.com",
"Contact"
),
),
br(
br(
form(
_method="get", _action="//hn.algolia.com/",
"Search:",
input(
_type="text", _name="q", _value="", _size="17", _autocorrect="off", _spellcheck="false", _autocapitalize="off", _autocomplete="false",
),
),
),
),
),
),
),
),