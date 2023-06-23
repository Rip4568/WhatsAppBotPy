from playwright.sync_api import sync_playwright
from celery import Celery, shared_task
from celery.schedules import crontab
import datetime
import time
celery = Celery('Bot', broker='pyamqp://guest@localhost//')


from playwright.sync_api import sync_playwright

@celery.on_after_configure.connect
def load_setup_celery_periodic_task(sender, **kw):

    sender.add_periodic_task(
        60,#segundos
        mandar_mensagens_periodicas.s(),
        name='mandar_mensagens_periodicas a ser executada...'
    )

""" @shared_task
def testar():
    return 'task periodica funcionando' """

@shared_task
def mandar_mensagens_periodicas():
	with sync_playwright() as session:
		user_dir_data = 'C:/Users/user/Desktop/Coisas/Programacao/Python/testes/WhatsappBOTtest/user_data'
		navegador = session.firefox.launch_persistent_context(user_data_dir=user_dir_data,headless=False)
		pagina = navegador.new_page()
		pagina.goto('https://web.whatsapp.com/')
		#Fazer um observador de mensagens aqui, sempre que alguem amndar alguma
		# mensagem ler e veriificar se contem algum parametro de funcao	
			

		def mandar_mensagem(destinatario:str='', mensagem:str='', repetir:int=1>0) -> bool:
			try:
				#localizar a pessoa pela barra de pesquisa
				pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/p').fill(destinatario)
				#seleciona a primeira pessoa que aparecer como resultado
				pagina.locator(selector=f'.matched-text:has-text("{destinatario}")').click()
				for _ in range(0,repetir):
					#localiza a barra de mandar/escrever mensagem
					pagina.locator(selector='xpath=//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').fill(mensagem)
					#clica no botão enviar mensagem
					pagina.click(selector='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
				return True
			except Exception as e:
				print(e)
				return False
		mensagem = f"Olá, estou mandando mensagem agora as {datetime.datetime.now()}, a proxima vez que irei mandar mensagem sera as {datetime.datetime.now() + datetime.timedelta(seconds=60)}"
		mandar_mensagem(destinatario='Lembrete', mensagem=mensagem, repetir=1)
	#espere 5 segundos antes de fechar novamente
		time.sleep(5)