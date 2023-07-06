# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from clusterMetrics import *
from constant import *
from storageMetrics import *


# -------- TELEMETRY RETRIEVAL FROM DUCKDB -------- #

# Fetches all experiment data from a duckdb connection. Adds a column 'exp_name'
# with the experiment identifier as value.
def retrieve_event_df(con, id, start_time):
    end_time = con.execute(
        "SELECT event_end_time FROM experiment_telemetry WHERE event_id=? and event_start_time=?;",
        [id, start_time]).df()['event_end_time'].item()
    df = con.execute(
        "SELECT * FROM experiment_telemetry WHERE event_start_time >= ? AND event_end_time <= ? order by event_start_time asc;",
        [start_time, end_time]).df()
    return df

def retrieve_grouped_event_df(con, id, start_time, filter_ids):
    # Extract relevant phase data.
    df = retrieve_event_df(con, id, start_time)
    df = filterByEventIds(df, filter_ids)

    grouped_df = pd.DataFrame()
    for idx, row in df.iterrows():
        event_df = retrieve_event_df(con, row['event_id'], row['event_start_time'])
        event_df["group_name"] = row['event_id']
        grouped_df = pd.concat([grouped_df, event_df])
    return grouped_df


# -------- TELEMETRY RETRIEVAL FROM DF -------- #

def filterByEventType(df, type):
    return df[df['event_type'] == type]

def filterByEventIds(df, ids):
    return df[df['event_id'].isin(ids)]

def filterByEventPrefix(df, id):
    return df[df['event_id'].str.startswith(id)]

# -------- TELEMETRY EXTRACTION -------- #

def get_storage_metrics(type, df, storage_path):
    if type=="AZURE":
        return AzureStorageMetrics(df, storage_path)
    else:
        return StorageMetrics(df, storage_path)
    
def get_cluster_metrics(type, df, cluster_name):
    if type=="AZURE":
        return AzureClusterMetrics(df, cluster_name)
    else:
        return ClusterMetrics(df, cluster_name)


# -------- DATE MANIPULATIONS -------- #

utc_format='%Y-%m-%dT%H:%M:%S.%f'
def time_diff_in_minutes(time_str1, time_str2):
    # Remove 'Z' at the end
    time_str1 = time_str1[:-1]
    time_str2 = time_str2[:-1]

    # Shorten if string is too long for parsing
    if len(time_str1) == 26:
        time_str1 = time_str1[:-3]
    if len(time_str2) == 26:
        time_str2 = time_str2[:-3]
    
    # Parse in utc format
    d1 = datetime.strptime(time_str1, utc_format)
    d2 = datetime.strptime(time_str2, utc_format)
    return abs((d2 - d1).seconds/60)


# -------- STRING/INTEGER MANIPULATIONS -------- #

def adjust_phase_names(str):
    return str.replace("single_user_", "SU-")
