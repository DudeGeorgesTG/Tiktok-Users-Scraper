import asyncio
import aiohttp
import os
import urllib.parse
import random
import binascii
import uuid
import time
import json
from datetime import datetime

class TikTokCollector:
    def __init__(self):
        self.processed_users = set()
        self.user_queue = asyncio.Queue()
        self.counter = 0
        self.lock = asyncio.Lock()
        self.save_lock = asyncio.Lock()
        self.num_workers = 250
        self.num_searchers = 15
        self._init_output_file()
    
    def _init_output_file(self):
        with open('scraped.json', 'w', encoding='utf-8') as f:
            f.write('')
    
    def generate_signature(self):
        timestamp = str(int(time.time()))
        return {
            'x-ss-req-ticket': str(int(time.time() * 1000)),
            'x-khronos': timestamp
        }
    
    def generate_ms_token(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
        return ''.join(random.choice(chars) for _ in range(120))
    
    def get_base_params(self):
        timestamp = str(int(time.time() * 1000))
        params = {
            "manifest_version_code": "330802",
            "_rticket": timestamp,
            "app_language": "ar",
            "app_type": "normal",
            "iid": str(random.randint(1, 10 ** 19)),
            "channel": "googleplay",
            "device_type": "RMX3511",
            "language": "ar",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "resolution": "1080*2236",
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "update_version_code": "330802",
            "ac2": "lte",
            "cdid": str(uuid.uuid4()),
            "sys_region": "IQ",
            "os_api": "33",
            "timezone_name": "Asia/Baghdad",
            "dpi": "360",
            "carrier_region": "IQ",
            "ac": "4g",
            "device_id": str(random.randint(1, 10 ** 19)),
            "os_version": "13",
            "timezone_offset": "10800",
            "version_code": "330802",
            "app_name": "musically_go",
            "ab_version": "33.8.2",
            "version_name": "33.8.2",
            "device_brand": "realme",
            "op_region": "IQ",
            "ssmix": "a",
            "device_platform": "android",
            "build_number": "33.8.2",
            "region": "IQ",
            "aid": "1340",
            "ts": timestamp
        }
        headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)'
        }
        return params, headers
    
    def generate_random_username(self):
        chars = 'qwertyuiopasdfghjklzxcvbnm1234567890_.'
        return ''.join(random.choice(chars) for _ in range(random.randint(2, 9)))
    
    async def save_account(self, account_data):
        async with self.save_lock:
            with open('scraped.json', 'a', encoding='utf-8') as f:
                json.dump(account_data, f, ensure_ascii=False)
                f.write('\n')
                f.flush()
                os.fsync(f.fileno())
    
    async def get_following(self, session, user_id):
        token = None
        while True:
            try:
                params, headers = self.get_base_params()
                query_string = urllib.parse.urlencode(params)
                signed = self.generate_signature()
                headers.update(signed)
                
                url = f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&count=50&source_type=1&request_tag_from=h5&{query_string}'
                if token:
                    url += f"&page_token={urllib.parse.quote(token)}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Error: Status {response.status}")
                        break
                    data = await response.json()
                
                saved_count = 0
                for user in data.get("followings", []):
                    username = user.get("unique_id", "")
                    user_id_found = user.get("uid", "")
                    
                    if username and username not in self.processed_users:
                        account_data = {
                            "username": username,
                            "user_id": user_id_found,
                            "nickname": user.get("nickname", ""),
                            "signature": user.get("signature", ""),
                            "bio": user.get("bio", ""),
                            "follower_count": user.get("follower_count", 0),
                            "following_count": user.get("following_count", 0),
                            "like_count": user.get("like_count", 0),
                            "video_count": user.get("aweme_count", 0),
                            "verified": user.get("verified", False),
                            "private": user.get("private", False),
                            "profile_picture_url": user.get("avatar_thumb", {}).get("url_list", [""])[0] if user.get("avatar_thumb") else "",
                            "region": user.get("region", ""),
                            "sec_uid": user.get("sec_uid", ""),
                            "total_favorited": user.get("total_favorited", 0),
                            "collected_at": datetime.now().isoformat()
                        }
                        
                        async with self.lock:
                            self.counter += 1
                            self.processed_users.add(username)
                            print(f'{self.counter} - {username} (ID: {user_id_found}) | {account_data["follower_count"]} followers | {account_data["following_count"]} following')
                        
                        await self.save_account(account_data)
                        saved_count += 1
                
                print(f"Saved {saved_count} accounts from this page")
                
                if not data.get("has_more"):
                    break
                token = data.get("next_page_token")
                if not token:
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
    
    async def search_users(self, session):
        while True:
            try:
                username = self.generate_random_username()
                timestamp = str(int(time.time() * 1000))
                iid = str(random.randint(1, 10 ** 19))
                device_id = str(random.randint(1, 10 ** 19))
                openudid = str(binascii.hexlify(os.urandom(8)).decode())
                cdid = str(uuid.uuid4())
                ms_token = self.generate_ms_token()
                
                url = f"https://search16-normal-c-alisg.tiktokv.com/aweme/v1/search/user/sug/?iid={iid}&device_id={device_id}&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid={openudid}&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket={timestamp}&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts={timestamp}&cdid={cdid}"
                
                payload = {
                    'keyword': username,
                    'count': "100",
                    'source': "tt_ffp_add_friends",
                    'mention_type': "0"
                }
                
                signed = self.generate_signature()
                headers = {
                    'Host': 'search16-normal-c-alisg.tiktokv.com',
                    'User-Agent': "com.zhiliaoapp.musically/2023105030 (Linux; U; Android 13; ar_IQ; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:2fdb62f9 2023-09-06 QuicVersion:bb24d47c 2023-07-19)",
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': f'msToken="{ms_token}"',
                    'x-ss-req-ticket': signed['x-ss-req-ticket'],
                    'x-khronos': signed['x-khronos'],
                }
                
                async with session.post(url, data=payload, headers=headers) as response:
                    if response.status != 200:
                        continue
                    data = await response.json()
                
                for item in data.get("sug_list", []):
                    try:
                        extra = item.get("extra_info", {})
                        username_found = extra.get("sug_uniq_id")
                        user_id = extra.get("sug_user_id")
                        if username_found and user_id:
                            async with self.lock:
                                if username_found not in self.processed_users:
                                    self.processed_users.add(username_found)
                                    await self.user_queue.put(user_id)
                    except:
                        continue
            except:
                continue
    
    async def worker(self, session):
        while True:
            try:
                user_id = await self.user_queue.get()
                await self.get_following(session, user_id)
                self.user_queue.task_done()
            except:
                pass
    
    async def run(self):
        async with aiohttp.ClientSession() as session:
            workers = [asyncio.create_task(self.worker(session)) for _ in range(self.num_workers)]
            searchers = [asyncio.create_task(self.search_users(session)) for _ in range(self.num_searchers)]
            await asyncio.gather(*workers, *searchers)

if __name__ == '__main__':
    collector = TikTokCollector()
    asyncio.run(collector.run())
