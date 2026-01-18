package org.helio.cartorioapi;

import org.helio.cartorioapi.dto.AtribuicaosDTO;
import org.helio.cartorioapi.dto.AtribuicaosMinDTO;
import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.repositorios.AtribuicaoRepository;
import org.helio.cartorioapi.services.AtribuicaosServices;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.Arrays;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

class AtribuicaosServicesTest {

    @Mock
    private AtribuicaoRepository repository;

    @InjectMocks
    private AtribuicaosServices service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    void testFindAll() {
        // Preparar dados
        Atribuicaos atribuicao1 = new Atribuicaos();
        atribuicao1.setId("1");
        atribuicao1.setNome("Atribuicao 1");
        Atribuicaos atribuicao2 = new Atribuicaos();
        atribuicao2.setId("2");
        atribuicao2.setNome("Atribuicao 2");
        Page<Atribuicaos> page = new PageImpl<>(Arrays.asList(atribuicao1, atribuicao2));

        // Configurar o mock
        when(repository.findAllBy(any(Pageable.class))).thenReturn(page);

        // Executar o método
        Page<AtribuicaosMinDTO> result = service.findAll(PageRequest.of(0, 10));

        // Verificar o resultado
        assertEquals(2, result.getContent().size());
        assertEquals("Atribuicao 1", result.getContent().get(0).getNome());
        assertEquals("Atribuicao 2", result.getContent().get(1).getNome());
    }

    @Test
    void testFindById() {
        // Preparar dados
        Atribuicaos atribuicao = new Atribuicaos();
        atribuicao.setId("1");
        atribuicao.setNome("Atribuicao 1");

        // Configurar o mock
        when(repository.findById("1")).thenReturn(Optional.of(atribuicao));

        // Executar o método
        AtribuicaosDTO result = service.findById("1");

        // Verificar o resultado
        assertEquals("Atribuicao 1", result.getNome());
    }

    @Test
    void testInsert() {
        // Preparar dados
        AtribuicaosDTO dto = new AtribuicaosDTO();
        dto.setId("1");
        dto.setNome("Atribuicao 1");

        // Configurar o mock
        when(repository.findById(anyString())).thenReturn(Optional.empty());
        when(repository.findByNome(anyString())).thenReturn(Optional.empty());
        when(repository.save(any(Atribuicaos.class))).thenReturn(new Atribuicaos(dto));

        // Executar o método
        AtribuicaosDTO result = service.insert(dto);

        // Verificar o resultado
        assertEquals("Atribuicao 1", result.getNome());
    }

    @Test
    void testUpdate() {
        // Preparar dados
        AtribuicaosDTO dto = new AtribuicaosDTO();
        dto.setId("1");
        dto.setNome("Atribuicao Atualizada");

        // Configurar o mock
        Atribuicaos existing = new Atribuicaos();
        existing.setId("1");
        existing.setNome("Atribuicao 1");
        when(repository.findById("1")).thenReturn(Optional.of(existing));
        when(repository.findByNome(anyString())).thenReturn(Optional.empty());
        when(repository.save(any(Atribuicaos.class))).thenReturn(new Atribuicaos(dto));

        // Executar o método
        AtribuicaosDTO result = service.update("1", dto);

        // Verificar o resultado
        assertEquals("Atribuicao Atualizada", result.getNome());
    }

    @Test
    void testDelete() {
        // Configurar o mock
        doNothing().when(repository).deleteById(anyString());

        // Executar o método
        service.delete("1");

        // Verificar o resultado
        verify(repository, times(1)).deleteById("1");
    }
}

