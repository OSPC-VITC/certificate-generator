import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
from datetime import datetime


def create_certificate(template_img, name, output_path, cert_type, prize_rank=None, event_name=None, event_date=None, signers=None, speaker_details=None):
    img = template_img.copy()
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # Get image dimensions
    img_w, img_h = img.size
    
    title_font = ImageFont.truetype("Latinia.ttf", 170)
    name_font = ImageFont.truetype("Latinia.ttf", 100)
    header_font = ImageFont.truetype("Latinia.ttf", 60)
    details_font = ImageFont.truetype("Latinia.ttf", 50)
    sign_font = ImageFont.truetype("Latinia.ttf", 35)
    prize_font = ImageFont.truetype("Latinia.ttf", 75)
    speaker_font = ImageFont.truetype("Latinia.ttf", 45)

    # Add certificate type with vertical positioning
    cert_title = f"Of {cert_type}"
    title_bbox = draw.textbbox((0, 0), cert_title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    x = (img_w - title_w) / 2
    y = img_h/3
    draw.text((x, y), cert_title, fill=(0, 0, 0, 255), font=title_font)
    
    # Add prize rank if applicable
    if prize_rank:
        rank_text = f"{prize_rank} Prize"
        rank_bbox = draw.textbbox((0, 0), rank_text, font=prize_font)
        rank_w = rank_bbox[2] - rank_bbox[0]
        x = (img_w - rank_w) / 2
        y += title_h + 90
        draw.text((x, y), rank_text, fill=(0, 0, 0, 255), font=prize_font)
    
    presented_text = "THIS CERTIFICATE IS PROUDLY PRESENTED TO"
    presented_bbox = draw.textbbox((0, 0), presented_text, font=header_font)
    presented_w = presented_bbox[2] - presented_bbox[0]
    presented_h = presented_bbox[3] - presented_bbox[1]
    x = (img_w - presented_w) / 2
    y = img_h/2 - 30
    draw.text((x, y), presented_text, fill=(0, 0, 0, 255), font=header_font)
    
    # Add recipient name with proper spacing
    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_w = name_bbox[2] - name_bbox[0]
    name_h = name_bbox[3] - name_bbox[1]
    x = (img_w - name_w) / 2
    y = img_h/2 + 80
    
    draw.text((x, y), name, fill=(0, 0, 0, 255), font=name_font)
    
    # Draw underline 
    line_y = y + name_h + 30
    draw.line((img_w/4, line_y, 3*img_w/4, line_y), fill=(0, 0, 0, 255), width=2)
    
    # event details 
    if event_name and event_date:
        achievement_text = {
            "Excellence": "for outstanding achievement in",
            "Participation": "for participating in",
            "Appreciation": "for valuable contribution to"
        }
        event_text = f"{achievement_text.get(cert_type, 'for participating in')} {event_name} {'Event by OSPC'}"
        date_text = f"on {event_date.strftime('%B %d, %Y')} {'at VIT Chennai'}"
        
        event_bbox = draw.textbbox((0, 0), event_text, font=details_font)
        event_w = event_bbox[2] - event_bbox[0]
        x = (img_w - event_w) / 2
        y = line_y + 50
        draw.text((x, y), event_text, fill=(0, 0, 0, 255), font=details_font)
        
        date_bbox = draw.textbbox((0, 0), date_text, font=details_font)
        date_w = date_bbox[2] - date_bbox[0]
        x = (img_w - date_w) / 2
        y += 70
        draw.text((x, y), date_text, fill=(0, 0, 0, 255), font=details_font)

        # Add speaker details if provided
        if speaker_details and speaker_details['name']:
            speaker_text = f"Speaker: {speaker_details['name']}"
            if speaker_details['designation']:
                speaker_text += f" - {speaker_details['designation']}"
            
            speaker_bbox = draw.textbbox((0, 0), speaker_text, font=speaker_font)
            speaker_w = speaker_bbox[2] - speaker_bbox[0]
            x = (img_w - speaker_w) / 2
            y += 70  # Add some space after the date
            draw.text((x, y), speaker_text, fill=(0, 0, 0, 255), font=speaker_font)
    
    # signatures
    if signers:
        sig_y = img_h - 450  # Adjusted signature position
        spacing = img_w // (len(signers) + 1)
        
        for i, signer in enumerate(signers, 1):
            if signer['signature'] and signer['name'] and signer['post']:
                try:
                    # Process signature image
                    sig_img = Image.open(signer['signature'])
                    if sig_img.mode != 'RGBA':
                        sig_img = sig_img.convert('RGBA')
                    
                    # Resize signature while maintaining aspect ratio
                    sig_w, sig_h = sig_img.size
                    new_w = 200
                    new_h = int((new_w / sig_w) * sig_h)
                    sig_img = sig_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                    # Calculate position
                    x = spacing * i - (new_w // 2)
                    
                    # Paste signature with transparency
                    txt_layer.paste(sig_img, (x, sig_y), sig_img)
                except:
                    # If signature image fails, draw a line instead
                    x = spacing * i - 100
                    draw.line((x, sig_y + 50, x + 200, sig_y + 50), fill=(0, 0, 0, 255), width=1)
                
                # Add signature line
                line_y = sig_y + 100
                draw.line((x, line_y, x + 200, line_y), fill=(0, 0, 0, 255), width=1)
                
                # Add name and designation
                name_bbox = draw.textbbox((0, 0), signer['name'], font=sign_font)
                name_w = name_bbox[2] - name_bbox[0]
                post_bbox = draw.textbbox((0, 0), signer['post'], font=sign_font)
                post_w = post_bbox[2] - post_bbox[0]
                
                name_x = x + (200 - name_w) // 2
                post_x = x + (200 - post_w) // 2
                
                draw.text((name_x, line_y + 20), signer['name'], fill=(0, 0, 0, 255), font=sign_font)
                draw.text((post_x, line_y + 60), signer['post'], fill=(0, 0, 0, 255), font=sign_font)
    
    # Combine the text layer with the background
    final_img = Image.alpha_composite(img, txt_layer)
    
    # Convert to RGB for PDF saving
    final_img = final_img.convert('RGB')
    
    # Save as PDF
    final_img.save(output_path, "PDF", resolution=300.0)
    return output_path

def main():
    st.title("Certificate Generator")
    
    # Load default template
    try:
        template_img = Image.open("certificate_template.png")
    except:
        st.error("Default template not found. Please ensure certificate_template.png exists.")
        return
    
    # Certificate type selection
    cert_type = st.selectbox(
        "Select Certificate Type",
        ["Excellence", "Participation", "Appreciation"],
        help="Choose the type of certificate to generate"
    )
    
    # Event details
    col1, col2 = st.columns(2)
    with col1:
        event_name = st.text_input("Event Name")
    with col2:
        event_date = st.date_input("Event Date")
    
    # Speaker details
    st.header("Speaker Details")
    include_speaker = st.checkbox("Include Speaker Details")
    speaker_details = None
    
    if include_speaker:
        speaker_col1, speaker_col2 = st.columns(2)
        with speaker_col1:
            speaker_name = st.text_input("Speaker Name")
        with speaker_col2:
            speaker_designation = st.text_input("Speaker Designation")
        speaker_details = {
            'name': speaker_name,
            'designation': speaker_designation
        }
    
    # Signature details
    st.header("Signature Details")
    num_signers = st.number_input("Number of Signatories", min_value=0, max_value=2, value=2)
    
    signers = []

    if num_signers > 0:
        cols = st.columns(num_signers)
        
        for i, col in enumerate(cols):
            with col:
                st.subheader(f"Signatory {i+1}")
                name = st.text_input(f"Name", key=f"name_{i}")
                post = st.text_input(f"Designation", key=f"post_{i}")
                signature = st.file_uploader(
                    f"Signature Image (PNG with transparency)",
                    type=['png'],
                    help="Upload a PNG image with transparent background",
                    key=f"sig_{i}"
                )
                signers.append({
                    'name': name,
                    'post': post,
                    'signature': signature
                })
    else:
        st.write("No signatories selected.")
    
    # Names file upload
    st.header("Upload Names")
    names_file = st.file_uploader("Upload names file (CSV/XLSX)", type=['csv', 'xlsx'])
    
    if names_file:
        try:
            if names_file.name.endswith('.csv'):
                df = pd.read_csv(names_file)
            else:
                df = pd.read_excel(names_file)
            
            st.write("Preview of names:")
            st.write(df.head())
            
            name_column = st.selectbox("Select the column containing names:", df.columns)
            
            # Initialize session state for prize assignments if not exists
            if 'prize_assignments' not in st.session_state:
                st.session_state.prize_assignments = {}
            
            # Prize allocation section
            if cert_type == "Excellence":
                st.header("Prize Allocation")
                st.write("Select names for each prize category:")
                
                prize_cols = st.columns(3)
                current_selections = {}
                all_names = df[name_column].tolist()
                
                with prize_cols[0]:
                    first_prize = st.multiselect(
                        "First Prize Winners",
                        all_names,
                        default=[name for name, prize in st.session_state.prize_assignments.items() if prize == "First"]
                    )
                    for name in first_prize:
                        current_selections[name] = "First"
                
                with prize_cols[1]:
                    available_second = [n for n in all_names if n not in first_prize]
                    second_prize = st.multiselect(
                        "Second Prize Winners",
                        available_second,
                        default=[name for name, prize in st.session_state.prize_assignments.items() if prize == "Second"]
                    )
                    for name in second_prize:
                        current_selections[name] = "Second"
                
                with prize_cols[2]:
                    available_third = [n for n in all_names if n not in first_prize and n not in second_prize]
                    third_prize = st.multiselect(
                        "Third Prize Winners",
                        available_third,
                        default=[name for name, prize in st.session_state.prize_assignments.items() if prize == "Third"]
                    )
                    for name in third_prize:
                        current_selections[name] = "Third"
                
                st.session_state.prize_assignments = current_selections
                
                st.subheader("Current Prize Assignments")
                assignment_df = pd.DataFrame([
                    {"Name": name, "Prize": prize} 
                    for name, prize in current_selections.items()
                ])
                if not assignment_df.empty:
                    st.write(assignment_df)
            
            if st.button("Generate Certificates"):
                if not all(signer['signature'] for signer in signers):
                    st.error("Please upload all signature images before generating certificates.")
                    return
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    total_names = len(df)
                    
                    for index, row in df.iterrows():
                        name = str(row[name_column]).strip()
                        if not name:
                            continue
                        
                        prize_rank = None
                        if cert_type == "Excellence":
                            prize_rank = st.session_state.prize_assignments.get(name)
                            if not prize_rank:
                                continue
                            
                        status_text.text(f"Generating certificate for {name}...")
                        cert_buffer = io.BytesIO()
                        
                        try:
                            create_certificate(
                                template_img=template_img,
                                name=name,
                                output_path=cert_buffer,
                                cert_type=cert_type,
                                prize_rank=prize_rank,
                                event_name=event_name,
                                event_date=event_date,
                                signers=signers,
                                speaker_details=speaker_details
                            )
                            
                            filename = f"{name.replace(' ', '_')}_{cert_type.lower()}"
                            if prize_rank:
                                filename += f"_{prize_rank.lower()}"
                            filename += "_certificate.pdf"
                            
                            zip_file.writestr(filename, cert_buffer.getvalue())
                        except Exception as e:
                            st.error(f"Error generating certificate for {name}: {str(e)}")
                        
                        progress_bar.progress((index + 1) / total_names)
                
                zip_buffer.seek(0)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                st.download_button(
                    label="Download Certificates ZIP",
                    data=zip_buffer,
                    file_name=f"certificates_{timestamp}.zip",
                    mime="application/zip"
                )
                
        except Exception as e:
            st.error(f"An error occurred while processing the names file: {str(e)}")

main()