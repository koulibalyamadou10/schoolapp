from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import os
from io import BytesIO

def generate_academic_report_pdf(student, academic_records, grades=None):
    """
    Génère un bulletin de notes PDF pour un étudiant
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Contenu du document
    story = []
    
    # En-tête
    story.append(Paragraph("BULLETIN DE NOTES", title_style))
    story.append(Paragraph("Système de Gestion Scolaire - SchoolApp", normal_style))
    story.append(Spacer(1, 20))
    
    # Informations de l'étudiant
    story.append(Paragraph("INFORMATIONS DE L'ÉTUDIANT", heading_style))
    
    student_data = [
        ['Nom complet:', f"{student.first_name} {student.last_name}"],
        ['Numéro étudiant:', student.student_id],
        ['Classe:', student.student_class],
        ['Date de naissance:', student.birth_date.strftime('%d/%m/%Y')],
        ['Statut académique:', student.get_academic_status_display()],
        ['Date d\'impression:', datetime.now().strftime('%d/%m/%Y à %H:%M')]
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 3*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(student_table)
    story.append(Spacer(1, 20))
    
    # Dossiers académiques
    if academic_records:
        story.append(Paragraph("DOSSIERS ACADÉMIQUES", heading_style))
        
        for record in academic_records:
            # Titre du semestre
            semester_title = f"Année {record.academic_year} - {record.get_semester_display()}"
            story.append(Paragraph(semester_title, ParagraphStyle(
                'SemesterTitle',
                parent=styles['Heading3'],
                fontSize=12,
                spaceAfter=10,
                textColor=colors.HexColor('#2980b9')
            )))
            
            # Données du semestre
            semester_data = [
                ['Moyenne générale:', f"{record.average_grade}/20"],
                ['Rang de classe:', f"{record.class_rank}e"],
                ['Taux de présence:', f"{record.attendance_rate}%"],
            ]
            
            if record.comments:
                semester_data.append(['Commentaires:', record.comments])
            
            semester_table = Table(semester_data, colWidths=[2*inch, 3*inch])
            semester_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(semester_table)
            story.append(Spacer(1, 15))
    
    # Notes détaillées par matière (si disponibles)
    if grades:
        story.append(Paragraph("NOTES DÉTAILLÉES", heading_style))
        
        # Grouper les notes par matière
        grades_by_subject = {}
        for grade in grades:
            subject_name = grade.subject.name
            if subject_name not in grades_by_subject:
                grades_by_subject[subject_name] = []
            grades_by_subject[subject_name].append(grade)
        
        # Créer un tableau pour chaque matière
        for subject_name, subject_grades in grades_by_subject.items():
            story.append(Paragraph(f"Matière: {subject_name}", ParagraphStyle(
                'SubjectTitle',
                parent=styles['Heading4'],
                fontSize=11,
                spaceAfter=8,
                textColor=colors.HexColor('#27ae60')
            )))
            
            # Données des notes
            notes_data = [['Date', 'Note']]
            total_notes = 0
            count_notes = 0
            
            for grade in subject_grades:
                notes_data.append([
                    grade.date.strftime('%d/%m/%Y'),
                    f"{grade.grade}/20"
                ])
                total_notes += grade.grade
                count_notes += 1
            
            # Ajouter la moyenne
            if count_notes > 0:
                average = total_notes / count_notes
                notes_data.append(['MOYENNE', f"{average:.2f}/20"])
            
            notes_table = Table(notes_data, colWidths=[1.5*inch, 1.5*inch])
            notes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),
            ]))
            
            story.append(notes_table)
            story.append(Spacer(1, 15))
    
    # Pied de page
    story.append(Spacer(1, 30))
    story.append(Paragraph("Ce document a été généré automatiquement par le système SchoolApp.", 
                          ParagraphStyle(
                              'Footer',
                              parent=styles['Normal'],
                              fontSize=8,
                              alignment=TA_CENTER,
                              textColor=colors.grey
                          )))
    
    # Construire le PDF
    doc.build(story)
    
    # Retourner le buffer
    buffer.seek(0)
    return buffer

def create_pdf_response(student, academic_records, grades=None):
    """
    Crée une réponse HTTP avec le PDF généré
    """
    pdf_buffer = generate_academic_report_pdf(student, academic_records, grades)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bulletin_{student.student_id}_{student.last_name}.pdf"'
    response.write(pdf_buffer.getvalue())
    pdf_buffer.close()
    
    return response