from fastapi import HTTPException, status, Request
from . import mail_communicator
from . import schemas


    
class AccountActivationHandler:
    
    @classmethod
    def send_activation_mail(self, teacher: schemas.TeacherCreateResponse, password: str) -> bool:
        
        templates = self.generate_activation_mail(teacher, password)
        subject=f"[time-table-app-g14] Teacher credentials"
        recipient=teacher.email
        print(recipient)
        try:
            mail_communicator.MailCommunicator.send_mail(recipient, subject, templates)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while sending the mail"
            )
        
    @classmethod
    def generate_activation_mail(self, teacher:schemas.TeacherCreateResponse, password:str) -> dict:
        # return the mail created
        
        html_template = f"""
        <div class="container" style="text-align: center;">
            <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">Hello <span style="font-weight: bold; text-transform: capitalize;">{teacher.nom}</span></p>
            <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">Login    : {teacher.login}</p>
            <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">Password : {password}</p>
        </div>
		"""
        text_template = f"""
            Hello {teacher.nom}
            Login   : {teacher.login}
            Password: {password}            
		"""
        return {
            "html_template" : html_template,
            "text_template" : text_template
        }
        
    
    