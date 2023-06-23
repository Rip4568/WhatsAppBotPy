from playwright.sync_api import sync_playwright
from celery import Celery, shared_task, Task
from celery.schedules import crontab
import time

celery = Celery('MensagensPeriodicas', broker='pyamqp://guest@localhost//', backend='rpc://')

@celery.on_after_configure.connect
def load_setup_celery_periodic_task(sender, **kw):
    sender.add_periodic_task(
        crontab(minute=23),  # segundos
        mandar_mensagem.s(destinatario='Lembrete',mensagem='WHATSAPP AUTO',headless=False),
        name='task periodica acionada, enviando a cada 10s'
    )

destinatario_ultima_mensagem:str
""" 
configurar a variavel acima para usar a funcao enviar_mensagem_ja_selecionado """
@shared_task
def mandar_mensagem(destinatario:str, mensagem:str, repetir:int=1>0,headless:bool=True) -> bool:
    user_dir_data = 'C:/Users/user/Desktop/Coisas/Programacao/Python/testes/WhatsappBOTtest'
    with sync_playwright() as session:
        navegador = session.firefox.launch_persistent_context(user_data_dir=user_dir_data,headless=headless)
        pagina = navegador.new_page()
        pagina.goto('https://web.whatsapp.com/')
        #localizar a pessoa pela barra de pesquisa
        pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]').fill(destinatario)
        #seleciona a primeira pessoa que aparecer como resultado
        pagina.locator(selector=f'.matched-text:has-text("{destinatario}")').click()
        for _ in range(0,repetir):
            #localiza a barra de mandar/escrever mensagem
            pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').fill(mensagem)
            #clica no botão enviar mensagem
            pagina.click(selector='xpath=/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
        
        time.sleep(5)

@shared_task
def funcaoTeste(nome:str='default'):
    print('task funcaoTeste, {}'.format(nome))

""" por algum motivo essas funções estão causando loop """
#mandar_mensagem.s(destinatario='Lembrete',mensagem='funcionando',),
if __name__ == '__main__':
    mandar_mensagem(destinatario='Lembrete',mensagem='funcionando')