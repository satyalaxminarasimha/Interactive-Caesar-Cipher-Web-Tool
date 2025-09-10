from scapy.all import sniff
import datetime
import pandas as pd

log_file = "packet_log.txt"
csv_file = "packet_log.csv"
packet_data = []

def packet_callback(packet):
    """Processes and logs captured packets with real-time display and CSV export"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if packet.haslayer("IP"):
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst
    else:
        src_ip, dst_ip = "N/A", "N/A"

    protocol = packet.summary().split()[0]
    payload_data = packet["Raw"].load if packet.haslayer("Raw") else "No Payload"

    packet_data.append([timestamp, protocol, src_ip, dst_ip, payload_data])

    with open(log_file, "a") as log:
        log.write(f"{timestamp} | {protocol} | {src_ip} -> {dst_ip}\n")

    print(f"Packet captured: {timestamp} | {protocol} | {src_ip} -> {dst_ip}")

# Get user filter input
filter_protocol = input("Enter protocol filter (e.g., tcp, udp, icmp) or 'all': ").strip().lower()
protocol_filter = filter_protocol if filter_protocol != "all" else None

print(f"Capturing packets... Press **Ctrl+C** to stop.")
sniff(prn=packet_callback, filter=protocol_filter, store=False)

df = pd.DataFrame(packet_data, columns=["Timestamp", "Protocol", "Source IP", "Destination IP", "Payload Data"])
df.to_csv(csv_file, index=False)
print(f"\nPacket log saved to {csv_file}")