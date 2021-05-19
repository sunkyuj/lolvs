from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://en.wikipedia.org/wiki/Main_Page')
soup = BeautifulSoup(response, 'html.parser')
for anchor in soup.find_all('a'): # a 태그 다 찾아서
    print(anchor.get('href', '/')) # 출력

'''
<div class="champion-box champion-stats-player-ranking">
    <div class="champion-box-header">
        <div class="champion-box-header__title">
            <h4>카사딘 장인 랭킹</h4>
        </div>
        <div class="champion-box-header__more">
            <a href="/ranking/champions/name=kassadin" class="champion-box-header__link">
                <img src="//opgg-static.akamaized.net/images/site/champion/detail-icon.png" alt=""></a>
        </div>
    </div>
    <div class="champion-box-content">
        <table class="champion-stats-summary-ranking__table">
                                                                                <tbody><tr>
                        <th>1</th>
                        <td class="champion-stats-summary-ranking__table__summoner">
                            <a href="//www.op.gg/summoner/userName=LunaLina" target="_blank">
                                <img src="//opgg-static.akamaized.net/images/profile_icons/profileIcon4655.jpg?image=c_scale,q_auto,c_scale,w_32&amp;v=1518361200"> <span>LunaLina</span> </a>
                        </td>
                        <td class="champion-stats-summary-ranking__table__gamecount"><b>731</b> 게임</td>
                    </tr>
                                                                <tr>
                        <th>2</th>
                        <td class="champion-stats-summary-ranking__table__summoner">
                            <a href="//www.op.gg/summoner/userName=%EC%9D%91%EC%95%A0+%EB%82%98+%EC%B9%B4%EC%82%AC%EB%94%98" target="_blank">
                                <img src="//opgg-static.akamaized.net/images/profile_icons/profileIcon1439.jpg?image=c_scale,q_auto,c_scale,w_32&amp;v=1518361200"> <span>응애 나 카사딘</span> </a>
                        </td>
                        <td class="champion-stats-summary-ranking__table__gamecount"><b>389</b> 게임</td>
                    </tr>
                                                                <tr>
                        <th>3</th>
                        <td class="champion-stats-summary-ranking__table__summoner">
                            <a href="//www.op.gg/summoner/userName=%EB%8F%84%ED%8C%8D%EB%9E%84%EC%A5%90+fan" target="_blank">
                                <img src="//opgg-static.akamaized.net/images/profile_icons/profileIcon1.jpg?image=c_scale,q_auto,c_scale,w_32&amp;v=1518361200"> <span>도팍랄쥐 fan</span> </a>
                        </td>
                        <td class="champion-stats-summary-ranking__table__gamecount"><b>367</b> 게임</td>
                    </tr>
                                                                <tr>
                        <th>4</th>
                        <td class="champion-stats-summary-ranking__table__summoner">
                            <a href="//www.op.gg/summoner/userName=%EC%B9%B4%EC%82%AC%EB%94%94" target="_blank">
                                <img src="//opgg-static.akamaized.net/images/profile_icons/profileIcon1636.jpg?image=c_scale,q_auto,c_scale,w_32&amp;v=1518361200"> <span>카사디</span> </a>
                        </td>
                        <td class="champion-stats-summary-ranking__table__gamecount"><b>317</b> 게임</td>
                    </tr>
                                                                <tr>
                        <th>5</th>
                        <td class="champion-stats-summary-ranking__table__summoner">
                            <a href="//www.op.gg/summoner/userName=T1+soO" target="_blank">
                                <img src="//opgg-static.akamaized.net/images/profile_icons/profileIcon7.jpg?image=c_scale,q_auto,c_scale,w_32&amp;v=1518361200"> <span>T1 soO</span> </a>
                        </td>
                        <td class="champion-stats-summary-ranking__table__gamecount"><b>268</b> 게임</td>
                    </tr>
                                            </tbody></table>
    </div>
</div>
'''