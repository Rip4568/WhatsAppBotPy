from playwright.sync_api import sync_playwright
from celery import Celery, shared_task
from celery.schedules import crontab

celery = Celery('Main', broker='pyamqp://guest@localhost//')

@celery.on_after_configure.connect
def load_setup_celery_periodic_task(sender, **kw):

    sender.add_periodic_task(
        2.00,#segundos
        testar.s(),
        name='enviando task testar()'
    )

@shared_task
def testar():
    return 'task periodica funcionando'


def playwrightBOT():
    from playwright.sync_api import sync_playwright
    user_dir_data = 'C:/Users/user/Desktop/Coisas/Programacao/Python/testes/WhatsappBOTtest/user_data'
    opcao = ''
    with sync_playwright() as session:
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

        def mandar_mensagem_ja_selecionado(mensagem:str, repetir:int=1):
            try:
                for _ in range(repetir):
                    #localiza a barra de mandar/escrever mensagem
                    pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').fill(mensagem)
                    #clica no botão enviar mensagem
                    pagina.click(selector='xpath=/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
            except Exception as error:
                print(error)

        def marcar_todas_as_pessoas_do_grupo(nome_do_grupo:str=""):
            pass

            #Localiza o grupo pela barra de pesquisa
            pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]').fill(nome_do_grupo)
            #seleciona o primeiro elemento que correspondente a busca
            pagina.locator(selector=f'.matched-text:has-text("{nome_do_grupo}")').click()
            #NOVAS FEATURES
            #Clica na barra superior para acessar os detalhes do grupo
            pagina.locator(selector='xpath=/html/body/div[1]/div/div/div[4]/div/header').click()
            #esta é a classe que todos os usuarios do grupo possui, filtrar todos eles
            elementos = pagina.locator(selector='.lhggkp7q .ln8gz9je .rx9719la').all_inner_texts()
            print(f'elementos puros >> {elementos =}\n o tipo do elemento >>{type(elementos) =}')
            mandar_mensagem_ja_selecionado(mensagem=f'{elementos}')
        #TODO:Fazer um observado para ele todas ultimas mensagens, fazer com que receba o comando /all@all para listar todas as pessoas do grupo
        #TODO, FUNÇÃO PRINCIPAL, listar todos as pessoas do grupo e marcalas, acredito que esssa será mais facil

        while True:
            opcao = input('e(sair)\ng (marcar todas as pessoas do grupo)\nm(mandar mensagem)\nmj (mandar mensagem para pessoa/grupo ja seelecionado)\n>>')
            if opcao == 'e':
                break
            elif opcao == 'g':
                marcar_todas_as_pessoas_do_grupo(nome_do_grupo=input('Nome do grupo >>'))
            elif opcao == 'm':
                mandar_mensagem(destinatario=input('Destinatario >>'), mensagem=input("Mensagem >>"),repetir=int(input("Repetir >>")))
            elif opcao == 'mj':
                mandar_mensagem_ja_selecionado(mensagem=input('Mensagem >>'), repetir=int(input('Repetir >>')))

        pagina.close()

def home():
    playwrightBOT()

if __name__ == '__main__':
    home()